from __future__ import annotations

from decimal import Decimal


ROUNDING_TOLERANCE_PER_ROW = Decimal("0.01")


def compare_grouped_batch_metrics(
    athena_results: list[dict[str, str]],
    redshift_results: list[dict[str, str]],
) -> None:
    athena_by_group = {
        (
            row["group_type"],
            row["group_value"],
        ): row
        for row in athena_results
    }

    redshift_by_group = {
        (
            row["group_type"],
            row["group_value"],
        ): row
        for row in redshift_results
    }

    if athena_by_group.keys() != redshift_by_group.keys():
        athena_keys = set(athena_by_group)
        redshift_keys = set(redshift_by_group)

        missing_in_redshift = (
            athena_keys - redshift_keys
        )

        missing_in_athena = (
            redshift_keys - athena_keys
        )

        raise ValueError(
            "Batch grouped validation keys do not match. "
            f"Missing in Redshift="
            f"{sorted(missing_in_redshift)}, "
            f"Missing in Athena="
            f"{sorted(missing_in_athena)}"
        )

    errors: list[str] = []

    for group_key in athena_by_group:
        group_type, group_value = group_key

        athena = athena_by_group[group_key]
        redshift = redshift_by_group[group_key]

        athena_group_row_count = int(
            athena["group_row_count"]
        )
        redshift_group_row_count = int(
            redshift["group_row_count"]
        )

        if (
            athena_group_row_count
            != redshift_group_row_count
        ):
            errors.append(
                f"{group_type}={group_value} "
                f"group_row_count mismatch: "
                f"Athena={athena_group_row_count}, "
                f"Redshift={redshift_group_row_count}"
            )

        athena_source_count = int(
            athena["source_record_count"]
        )
        redshift_source_count = int(
            redshift["source_record_count"]
        )

        if athena_source_count != redshift_source_count:
            errors.append(
                f"{group_type}={group_value} "
                f"source_record_count mismatch: "
                f"Athena={athena_source_count}, "
                f"Redshift={redshift_source_count}"
            )

        monetary_tolerance = (
            Decimal(str(athena_group_row_count))
            * ROUNDING_TOLERANCE_PER_ROW
        )

        for metric_name in (
            "total_vouchers_paid",
            "total_vouchers_pending",
            "total_encumbrance_balance",
        ):
            athena_value = Decimal(
                athena[metric_name]
            )

            redshift_value = Decimal(
                redshift[metric_name]
            )

            difference = abs(
                athena_value - redshift_value
            )

            if difference > monetary_tolerance:
                errors.append(
                    f"{group_type}={group_value} "
                    f"{metric_name} mismatch: "
                    f"Athena={athena_value}, "
                    f"Redshift={redshift_value}, "
                    f"difference={difference}, "
                    f"tolerance={monetary_tolerance}"
                )

    if errors:
        raise ValueError(
            "Batch grouped cross-layer validation failed:\n"
            + "\n".join(errors)
        )

    print(
        "Batch grouped cross-layer validation: PASS"
    )