# pylint: disable=too-few-public-methods
class ReadOnlyAdminDateFields:
    readonly_fields = (
        "created_at",
        "updated_at",
        "deleted_at",
    )
