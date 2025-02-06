from rest_framework import serializers, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Client, Piece, Product, Budget

# Serializers

class PieceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Piece
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    piece = PieceSerializer()
    
    class Meta:
        model = Product
        fields = ['id', 'piece', 'image', 'size', 'pps', 'price', 'color']


class BudgetSerializer(serializers.ModelSerializer):
    total_q = serializers.ReadOnlyField()
    total = serializers.ReadOnlyField()
    
    class Meta:
        model = Budget
        fields = ['id', 'client', 'product', 'area', 'discount', 'total_q', 'total']


# Views

class PieceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Piece.objects.all()
    serializer_class = PieceSerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=False, methods=['get'])
    def sizes(self, request):
        """Devuelve las medidas disponibles para una pieza seleccionada"""
        piece_id = request.query_params.get('piece_id')
        if not piece_id:
            return Response({'error': 'Se requiere piece_id'}, status=400)
        
        sizes = Product.objects.filter(piece_id=piece_id).values_list('size', flat=True).distinct()
        return Response({'sizes': list(sizes)})

    @action(detail=False, methods=['get'])
    def colors(self, request):
        """Devuelve los colores disponibles para una pieza y medida seleccionadas"""
        piece_id = request.query_params.get('piece_id')
        size = request.query_params.get('size')
        
        if not piece_id or not size:
            return Response({'error': 'Se requieren piece_id y size'}, status=400)
        
        colors = Product.objects.filter(piece_id=piece_id, size=size).values_list('color', flat=True).distinct()
        return Response({'colors': list(colors)})


class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer

    @action(detail=False, methods=['post'])
    def calculate_budget(self, request):
        """Calcula el presupuesto sin necesidad de guardarlo en la base de datos"""
        piece_id = request.data.get('piece_id')
        size = request.data.get('size')
        color = request.data.get('color')
        area = request.data.get('area')
        discount = request.data.get('discount', False)
        
        try:
            product = Product.objects.get(piece_id=piece_id, size=size, color=color)
        except Product.DoesNotExist:
            return Response({'error': 'Producto no encontrado'}, status=404)
        
        total_q = product.pps * int(area)
        total = total_q * product.price
        
        return Response({
            'total_q': total_q,
            'total': total
        })
