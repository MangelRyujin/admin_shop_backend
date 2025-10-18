from rest_framework import serializers
from django.db import transaction
from apps.inventory.models import StockMovement, Stock
from apps.inventory.api.serializers.stock_serializer import StockSerializer

class StockMovementSerializer(serializers.ModelSerializer):
    stock_one_details = serializers.SerializerMethodField()
    stock_two_details = serializers.SerializerMethodField()
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = StockMovement
        fields = '__all__'
        read_only_fields = ('created_date', 'user')

    def get_stock_one_details(self, obj):
        """Esto es por si hace falta ver los detalles del primer stock"""
        return StockSerializer(obj.stock_one).data

    def get_stock_two_details(self, obj):
        """Esto es por si hace falta ver los detalles del segundo stock, si existe, sino na"""
        if obj.stock_two:
            return StockSerializer(obj.stock_two).data
        return None

    def validate(self, data):
        action_operation = data.get('action_operation')
        action_type = data.get('action_type')
        stock_one = data.get('stock_one')
        stock_two = data.get('stock_two')
        cant = data.get('cant')

        # Validación básica de cantidad
        if cant <= 0: # remove this validation "Model validate this field becouse your use MinValueValidator"
            raise serializers.ValidationError({
                'cant': 'La cantidad debe ser mayor a 0'
            })

        # Validaciones para MOVIMIENTOS SIMPLES (acción tipo 1)
        if action_type == '1':
            # En simples, stock_two debe ser None
            if stock_two is not None:
                raise serializers.ValidationError({
                    'stock_two': 'Para movimiento simple, stock_two debe estar vacío'
                })
            
            # Validar stock suficiente para SALIDAS
            if action_operation == '1' and stock_one.cant < cant:
                raise serializers.ValidationError({
                    'cant': f'Stock insuficiente en {stock_one.product.name}. Disponible: {stock_one.cant}, Solicitado: {cant}'
                })

        # Validaciones para MOVIMIENTOS MÚLTIPLES (acción tipo 2)
        elif action_type == '2':
            # Stock_two es obligatorio en múltiples
            if stock_two is None:
                raise serializers.ValidationError({
                    'stock_two': 'Para movimiento múltiple, stock_two es requerido'
                })

            # No puede ser el mismo stock
            if stock_one.id == stock_two.id:
                raise serializers.ValidationError({
                    'stock_two': 'No puede ser el mismo stock para movimientos múltiples'
                })

            # Deben ser el mismo producto
            if stock_one.product.id != stock_two.product.id:
                raise serializers.ValidationError({
                    'stock_two': 'Solo se pueden transferir stocks del mismo producto'
                })

            # Validaciones de stock según operación
            if action_operation == '1':
                # SALIDA MÚLTIPLE: stock_one pierde, stock_two gana
                if stock_one.cant < cant:
                    raise serializers.ValidationError({
                        'cant': f'Stock insuficiente en origen. Disponible: {stock_one.cant}, Solicitado: {cant}'
                    })
            else:
                # ENTRADA MÚLTIPLE: stock_one gana, stock_two pierde  
                if stock_two.cant < cant:
                    raise serializers.ValidationError({
                        'cant': f'Stock insuficiente en destino. Disponible: {stock_two.cant}, Solicitado: {cant}'
                    })

        return data

    def create(self, validated_data):
        with transaction.atomic():
            validated_data['user'] = self.context['request'].user
            
            movement = StockMovement.objects.create(**validated_data)
            
            # Actualizar las cantidades de stock según el tipo de movimiento
            self._update_stock_quantities(movement)
            
            return movement

    def _update_stock_quantities(self, movement):
        # MOVIMIENTO SIMPLE
        if movement.action_type == '1':
            if movement.action_operation == '1':  # SALIDA
                movement.stock_one.cant -= movement.cant
            else:  # ENTRADA
                movement.stock_one.cant += movement.cant
            movement.stock_one.save()

        # MOVIMIENTO MÚLTIPLE  
        else:
            if movement.action_operation == '1':  # SALIDA
                # stock_one pierde, stock_two gana
                movement.stock_one.cant -= movement.cant
                movement.stock_two.cant += movement.cant
            else:  # ENTRADA
                # stock_one gana, stock_two pierde
                movement.stock_one.cant += movement.cant
                movement.stock_two.cant -= movement.cant
            
            movement.stock_one.save()
            movement.stock_two.save()

class StockMovementCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMovement
        fields = ['action_operation', 'action_type', 'motive', 'description', 'cant', 'stock_one', 'stock_two']

    def validate_cant(self, value):
        if value <= 0:
            raise serializers.ValidationError("La cantidad debe ser mayor a 0")
        return value