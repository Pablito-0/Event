from django.contrib import admin, messages

from event.models import Company, Event, Ticket

admin.site.register(Company)

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    search_fields = ("vip", "event", "number", "user")
    list_display = ("event", "vip", "user")
    list_filter = ("vip",)
    list_per_page = 100
    list_max_show_all = 200

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        if form.cleaned_data["ticket_count"] < form.initial["ticket_count"]:
            messages.warning(
                request,
                f"Ticket count should be greater than initial value, so we set it to {form.initial['ticket_count']}",
            )
        super().save_model(request, obj, form, change)