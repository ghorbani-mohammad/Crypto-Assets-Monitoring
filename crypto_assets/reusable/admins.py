class ReadOnlyAdminDateFields:
    readonly_fields = (
        "created_at",
        "updated_at",
        "deleted_at",
    )

    def plus_field(self, field: str):
        # return default readonly_fields + field
        return self.readonly_fields + (field,)

    def minus_field(self, field: str):
        # return default readonly_fields - field
        return tuple(f for f in self.readonly_fields if f != field)
