from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    coin = serializers.CharField(source='coin.code', read_only=True)
    current_value = serializers.FloatField(source='get_current_value', read_only=True)
    change_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'type', 'market', 'coin', 'price', 
            'quantity', 'total_price', 'current_value',
            'date', 'change_percentage'
        ]
        read_only_fields = fields
    
    def get_change_percentage(self, obj):
        if obj.type == Transaction.BUY:
            return obj.get_change_percentage
        return None
    
    def to_representation(self, instance):
        from .views import format_number
        ret = super().to_representation(instance)
        
        # Format numeric fields
        for field in ['price', 'quantity', 'total_price', 'current_value', 'change_percentage']:
            if ret[field] is not None:
                ret[field] = format_number(ret[field])
        
        # Format date
        if instance.jdate:
            ret['date'] = instance.jdate.strftime('%Y-%m-%d %H:%M:%S')
        else:
            ret['date'] = None
            
        return ret
