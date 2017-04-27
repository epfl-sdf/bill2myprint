from django.contrib import admin


from .models import ServiceconsumerT, BudgettransactionsT, GroupmembershipT, ConsumeridentitiesT


class ServiceconsumerTAdmin(admin.ModelAdmin):
    readonly_fields = [f.name for f in ServiceconsumerT._meta.fields]
    list_display = ('id', 'name', 'login', 'addressone', 'defaultgroupid', 'defaultcostcenter')
    search_fields = ['id', 'name', 'login', 'addressone', 'defaultgroupid', 'defaultcostcenter', 'emailaddress']

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class BudgettransactionsTAdmin(admin.ModelAdmin):
    readonly_fields = [f.name for f in BudgettransactionsT._meta.fields]
    list_display = list([f.name for f in BudgettransactionsT._meta.fields])
    list_display_links = (None)
    search_fields = ['entity__id', 'entity__name', 'entity__login', 'serviceusage']

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class GroupmembershipTAdmin(admin.ModelAdmin):
    readonly_fields = [f.name for f in GroupmembershipT._meta.fields]
    list_display = ('user', 'group')
    list_display_links = (None)
    search_fields = ['user__name', 'user__id', 'user__login', 'group__name', 'group__id', 'group__login']

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ConsumeridentitiesTAdmin(admin.ModelAdmin):
    readonly_fields = [f.name for f in ConsumeridentitiesT._meta.fields]
    list_display = ('id', 'consumerid', 'value')
    list_display_links = (None)
    search_fields = ['id', 'value']

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(ServiceconsumerT, ServiceconsumerTAdmin)
admin.site.register(BudgettransactionsT, BudgettransactionsTAdmin)
admin.site.register(GroupmembershipT, GroupmembershipTAdmin)
admin.site.register(ConsumeridentitiesT, ConsumeridentitiesTAdmin)
