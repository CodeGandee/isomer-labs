(function () {
  function textOf(node) {
    return (node.textContent || "").trim();
  }

  function classifyLabel(label, blockquote) {
    var labelText = textOf(label).replace(/\s+/g, " ");
    var blockText = textOf(blockquote);
    if (labelText === "AI:") {
      return "chatlog-ai-response";
    }
    if (labelText === "User Prompt:") {
      return "chatlog-user-prompt";
    }
    if (labelText === "User Action:" && /cancel|interrupt/i.test(blockText)) {
      return "chatlog-user-interruption";
    }
    if (labelText === "User Action:") {
      return "chatlog-user-action";
    }
    return "";
  }

  function decorateChatlogs() {
    var article = document.querySelector("article.md-content__inner");
    if (!article || !location.pathname.includes("/topic-chatlogs/")) {
      return;
    }
    document.body.classList.add("chatlog-page");
    article.querySelectorAll("p").forEach(function (label) {
      var labelText = textOf(label).replace(/\s+/g, " ");
      if (!/^(User Prompt:|User Action:|AI:)$/.test(labelText)) {
        return;
      }
      var next = label.nextElementSibling;
      while (next && next.tagName !== "BLOCKQUOTE") {
        next = next.nextElementSibling;
      }
      if (!next) {
        return;
      }
      var className = classifyLabel(label, next);
      if (!className) {
        return;
      }
      label.classList.add("chatlog-label");
      next.classList.add("chatlog-block", className);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", decorateChatlogs);
  } else {
    decorateChatlogs();
  }
})();
