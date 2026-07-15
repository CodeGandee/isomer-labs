from __future__ import annotations

import unittest

from isomer_labs.core.artifact_identity import (
    ArtifactIdentityError,
    extension_id_for_skill,
    extension_namespace_for_skill,
    packaged_extension_ids,
    packaged_extension_namespaces,
    parse_artifact_identity,
    valid_artifact_identity,
)


class ArtifactIdentityTests(unittest.TestCase):
    def test_canonical_identity_round_trips_exactly(self) -> None:
        identity = parse_artifact_identity(
            "DEEPSCI:MAIN-RUN-RECORD",
            expected_extension="deepsci",
            known_extensions=packaged_extension_ids(),
        )
        self.assertEqual("DEEPSCI", identity.namespace)
        self.assertEqual("deepsci", identity.extension_id)
        self.assertEqual("MAIN-RUN-RECORD", identity.what)
        self.assertEqual("DEEPSCI:MAIN-RUN-RECORD", identity.value)
        self.assertTrue(valid_artifact_identity(identity.value))

    def test_manifest_owns_namespaces_and_skill_prefixes(self) -> None:
        self.assertEqual(frozenset({"deepsci", "kaoju"}), packaged_extension_ids())
        self.assertEqual(frozenset({"DEEPSCI", "KAOJU"}), packaged_extension_namespaces())
        self.assertEqual("deepsci", extension_id_for_skill("isomer-deepsci-analysis"))
        self.assertEqual("DEEPSCI", extension_namespace_for_skill("isomer-deepsci-analysis"))
        self.assertEqual("kaoju", extension_id_for_skill("isomer-kaoju-frame"))
        self.assertEqual("KAOJU", extension_namespace_for_skill("isomer-kaoju-frame"))
        self.assertIsNone(extension_id_for_skill("isomer-op-topic-creator"))
        self.assertIsNone(extension_namespace_for_skill("isomer-op-topic-creator"))

    def test_noncanonical_values_are_rejected_without_normalization(self) -> None:
        cases = (
            "<DEEPSCI:MAIN-RUN-RECORD>",
            "[[DEEPSCI:MAIN-RUN-RECORD]]",
            "DEEPSCI:MAIN_RUN_RECORD",
            "MAIN-RUN-RECORD",
            "pipeline-run-record",
            "deepsci:main-run-record",
            "DeepSci:MAIN-RUN-RECORD",
            "DEEPSCI:Main-Run-Record",
            "KAOJU:SURVEY_CONTRACT",
        )
        for value in cases:
            with self.subTest(value=value), self.assertRaises(ArtifactIdentityError) as caught:
                parse_artifact_identity(value)
            self.assertEqual("invalid_artifact_identity", caught.exception.code)
            self.assertEqual(value, caught.exception.value)
            self.assertFalse(hasattr(caught.exception, "canonical_recovery"))
            self.assertFalse(valid_artifact_identity(value))

    def test_wrong_and_unknown_namespaces_are_rejected_without_recovery(self) -> None:
        with self.assertRaises(ArtifactIdentityError) as mismatch:
            parse_artifact_identity("KAOJU:SURVEY-CONTRACT", expected_extension="deepsci")
        self.assertEqual("artifact_identity_extension_mismatch", mismatch.exception.code)
        self.assertEqual("deepsci", mismatch.exception.expected_extension)
        self.assertEqual("DEEPSCI", mismatch.exception.expected_namespace)
        self.assertFalse(hasattr(mismatch.exception, "canonical_recovery"))

        with self.assertRaises(ArtifactIdentityError) as unknown:
            parse_artifact_identity("UNKNOWN:ARTIFACT", known_extensions=packaged_extension_ids())
        self.assertEqual("unknown_artifact_identity_extension", unknown.exception.code)
        self.assertFalse(hasattr(unknown.exception, "canonical_recovery"))


if __name__ == "__main__":
    unittest.main()
