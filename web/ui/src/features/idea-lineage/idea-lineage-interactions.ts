import { merge, of, Subject, Subscription, timer } from "rxjs";
import { filter, map, switchMap, take, takeUntil } from "rxjs/operators";
import type { IdeaFlowNodeData } from "../../graph-utils";
import type { IdeaLineageAction, IdeaLineageHoverSessionId, IdeaLineageStore } from "./idea-lineage-state";

export type IdeaLineageHoverEvent = {
  nodeId: string;
  data: IdeaFlowNodeData;
  x: number;
  y: number;
};

export type IdeaLineageNodeEvent = {
  nodeId: string;
};

export type IdeaLineageTouchStartEvent = IdeaLineageHoverEvent & {
  pointerId: number;
};

export type IdeaLineageTouchMoveEvent = {
  pointerId: number;
  x: number;
  y: number;
};

export type IdeaLineageTouchEndEvent = {
  pointerId: number;
};

export type IdeaLineageInteractionBoundary = {
  nodeEnter: (event: IdeaLineageHoverEvent) => void;
  nodeMove: (event: IdeaLineageHoverEvent) => void;
  nodeLeave: (event: IdeaLineageNodeEvent) => void;
  nodeClick: (event: IdeaLineageNodeEvent) => void;
  nodeOpen: (event: IdeaLineageNodeEvent) => void;
  tooltipEnter: () => void;
  tooltipLeave: () => void;
  touchLongPressStart: (event: IdeaLineageTouchStartEvent) => void;
  touchLongPressMove: (event: IdeaLineageTouchMoveEvent) => void;
  touchLongPressEnd: (event: IdeaLineageTouchEndEvent) => void;
  closeHover: () => void;
  dispose: () => void;
};

export type IdeaLineageInteractionBoundaryOptions = {
  store: IdeaLineageStore;
  getHoverPreviewDelayMs: () => number;
  hoverPreviewCloseDelayMs: number;
  touchLongPressMoveTolerancePx: number;
};

export function createIdeaLineageInteractionBoundary({
  store,
  getHoverPreviewDelayMs,
  hoverPreviewCloseDelayMs,
  touchLongPressMoveTolerancePx,
}: IdeaLineageInteractionBoundaryOptions): IdeaLineageInteractionBoundary {
  const nodeEnter$ = new Subject<IdeaLineageHoverEvent>();
  const nodeMove$ = new Subject<IdeaLineageHoverEvent>();
  const nodeLeave$ = new Subject<IdeaLineageNodeEvent>();
  const nodeClick$ = new Subject<IdeaLineageNodeEvent>();
  const nodeOpen$ = new Subject<IdeaLineageNodeEvent>();
  const tooltipEnter$ = new Subject<void>();
  const tooltipLeave$ = new Subject<void>();
  const touchStart$ = new Subject<IdeaLineageTouchStartEvent>();
  const touchMove$ = new Subject<IdeaLineageTouchMoveEvent>();
  const touchEnd$ = new Subject<IdeaLineageTouchEndEvent>();
  const dispose$ = new Subject<void>();
  const subscription = new Subscription();
  let disposed = false;
  let nextHoverSessionId = 1;

  const nextSessionId = () => nextHoverSessionId++;
  const dispatch = (action: IdeaLineageAction) => store.dispatch(action);

  subscription.add(
    nodeEnter$
      .pipe(
        switchMap((enter) => {
          const sessionId = nextSessionId();
          const sameNode = (event: IdeaLineageNodeEvent) => event.nodeId === enter.nodeId;
          const sameMoveNode = (event: IdeaLineageHoverEvent) => event.nodeId === enter.nodeId;
          const click$ = nodeClick$.pipe(filter(sameNode), take(1));
          const open$ = nodeOpen$.pipe(filter(sameNode), take(1));
          const leave$ = nodeLeave$.pipe(filter(sameNode), take(1));
          const terminal$ = merge(click$, open$, leave$, dispose$).pipe(take(1));
          const nextEnter$ = nodeEnter$.pipe(take(1));
          const closeCancel$ = merge(tooltipEnter$, nextEnter$, dispose$);
          const immediateClose$ = merge(click$, open$).pipe(map(() => hoverClosed(sessionId)));
          const closeAfterNodeLeave$ = leave$.pipe(
            switchMap(() => timer(hoverPreviewCloseDelayMs).pipe(takeUntil(closeCancel$), map(() => hoverClosed(sessionId)))),
          );
          const closeAfterTooltipLeave$ = tooltipLeave$.pipe(
            switchMap(() => timer(hoverPreviewCloseDelayMs).pipe(takeUntil(closeCancel$), map(() => hoverClosed(sessionId)))),
            takeUntil(merge(click$, open$, nextEnter$, dispose$)),
          );

          return merge(
            of<IdeaLineageAction>({ type: "hoverStarted", sessionId, preview: enter }),
            nodeMove$.pipe(filter(sameMoveNode), takeUntil(terminal$), map((event) => ({ type: "hoverMoved", sessionId, preview: event }) satisfies IdeaLineageAction)),
            timer(getHoverPreviewDelayMs()).pipe(takeUntil(terminal$), map(() => ({ type: "hoverDelayElapsed", sessionId }) satisfies IdeaLineageAction)),
            immediateClose$,
            closeAfterNodeLeave$,
            closeAfterTooltipLeave$,
          );
        }),
        takeUntil(dispose$),
      )
      .subscribe(dispatch),
  );

  subscription.add(
    touchStart$
      .pipe(
        switchMap((start) => {
          const sessionId = nextSessionId();
          const sameMovePointer = (event: IdeaLineageTouchMoveEvent) => event.pointerId === start.pointerId;
          const sameEndPointer = (event: IdeaLineageTouchEndEvent) => event.pointerId === start.pointerId;
          const movedTooFar$ = touchMove$.pipe(
            filter(sameMovePointer),
            filter((event) => Math.hypot(event.x - start.x, event.y - start.y) > touchLongPressMoveTolerancePx),
            take(1),
          );
          const ended$ = touchEnd$.pipe(filter(sameEndPointer), take(1));
          const cancel$ = merge(movedTooFar$, ended$, nodeClick$, nodeOpen$, dispose$).pipe(take(1));

          return merge(
            of<IdeaLineageAction>({
              type: "touchLongPressStarted",
              pointerId: start.pointerId,
              nodeId: start.nodeId,
              data: start.data,
              x: start.x,
              y: start.y,
            }),
            timer(getHoverPreviewDelayMs()).pipe(takeUntil(cancel$), map(() => ({ type: "touchLongPressElapsed", pointerId: start.pointerId, sessionId }) satisfies IdeaLineageAction)),
            cancel$.pipe(map(() => ({ type: "touchLongPressCanceled", pointerId: start.pointerId }) satisfies IdeaLineageAction)),
          );
        }),
        takeUntil(dispose$),
      )
      .subscribe(dispatch),
  );

  const completeSubjects = () => {
    nodeEnter$.complete();
    nodeMove$.complete();
    nodeLeave$.complete();
    nodeClick$.complete();
    nodeOpen$.complete();
    tooltipEnter$.complete();
    tooltipLeave$.complete();
    touchStart$.complete();
    touchMove$.complete();
    touchEnd$.complete();
    dispose$.complete();
  };

  return {
    nodeEnter(event) {
      if (!disposed) {
        nodeEnter$.next(event);
      }
    },
    nodeMove(event) {
      if (!disposed) {
        nodeMove$.next(event);
      }
    },
    nodeLeave(event) {
      if (!disposed) {
        nodeLeave$.next(event);
      }
    },
    nodeClick(event) {
      if (!disposed) {
        nodeClick$.next(event);
        dispatch({ type: "nodeSelected", nodeId: event.nodeId });
      }
    },
    nodeOpen(event) {
      if (!disposed) {
        nodeOpen$.next(event);
        dispatch({ type: "nodeOpened", nodeId: event.nodeId });
      }
    },
    tooltipEnter() {
      if (!disposed) {
        tooltipEnter$.next();
      }
    },
    tooltipLeave() {
      if (!disposed) {
        tooltipLeave$.next();
      }
    },
    touchLongPressStart(event) {
      if (!disposed) {
        touchStart$.next(event);
      }
    },
    touchLongPressMove(event) {
      if (!disposed) {
        touchMove$.next(event);
      }
    },
    touchLongPressEnd(event) {
      if (!disposed) {
        touchEnd$.next(event);
      }
    },
    closeHover() {
      if (!disposed) {
        dispatch({ type: "hoverClosed" });
      }
    },
    dispose() {
      if (disposed) {
        return;
      }
      disposed = true;
      dispose$.next();
      dispatch({ type: "hoverClosed" });
      dispatch({ type: "touchLongPressCanceled" });
      subscription.unsubscribe();
      completeSubjects();
    },
  };
}

function hoverClosed(sessionId: IdeaLineageHoverSessionId): IdeaLineageAction {
  return { type: "hoverClosed", sessionId };
}
