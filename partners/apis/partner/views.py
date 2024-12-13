from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from core.models.partner import Partner
from core.models.referral_code import ReferralCode
from core.permissions.is_admin import IsAdminUserRole
from core.permissions.is_admin_or_owner import IsAdminOrOwner
from core.permissions.is_not_blacklisted import IsNotBlacklisted
from core.utils.pagination import CustomPagination
from core.utils.logger import exception_log
from core.utils.code_generator import generate_referral_code
from partners.serializers.partner.create import PartnerCreateSerializer
from partners.serializers.partner.update import PartnerUpdateSerializer
from partners.serializers.partner.read import PartnerReadSerializer


class PartnerViewSet(viewsets.ModelViewSet):
    queryset = Partner.objects.all()
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['partner_type', 'is_active']
    ordering_fields = ['name']
    search_fields = ['name', 'email']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return PartnerCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return PartnerUpdateSerializer
        return PartnerReadSerializer

    def get_permissions(self):
        if self.action in ['list', 'create', 'destroy']:
            return [IsAuthenticated(), IsNotBlacklisted(), IsAdminUserRole()]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            return [IsAuthenticated(), IsNotBlacklisted(), IsAdminOrOwner()]
        return []

    def finalize_response(self, request, response, *args, **kwargs):
        if not isinstance(response.data, dict):
            response.data = {
                "info": "UNEXPECTED_ERROR_OCCURRED",
                "errors": str(response.data)
            }
            return super().finalize_response(request, response, *args, **kwargs)
        
        if isinstance(response.data, dict) and 'info' in response.data:
            return super().finalize_response(request, response, *args, **kwargs)
        
        if response.status_code < 300:
            info = {
                'create': "PARTNER_CREATED_SUCCESSFULLY",
                'update': "PARTNER_UPDATED_SUCCESSFULLY",
                'partial_update': "PARTNER_UPDATED_SUCCESSFULLY",
                'retrieve': "PARTNER_RETRIEVED_SUCCESSFULLY",
                'list': "PARTNERS_LISTED_SUCCESSFULLY",
                'destroy': "PARTNER_DELETED_SUCCESSFULLY"
            }.get(self.action, "SUCCESS")
                    
            response.data = {
                "info": info,
                "data": response.data
            }
        else: 
            info = "UNEXPECTED_ERROR_OCCURRED"
            if isinstance(response.data, dict) and 'detail' in response.data:
                if isinstance(response.data['detail'], list) or isinstance(response.data['detail'], dict):
                    info = "VALIDATION_ERROR"
            elif response.status_code == 404:
                info = "PARTNER_NOT_FOUND"      
                 
            response.data = {
                "info": info,
                "errors": response.data 
            } 
        return super().finalize_response(request, response, *args, **kwargs)
    
    def perform_create(self, serializer):
        partner = serializer.save()
        try:
            partner_referral_code = generate_referral_code(partner.name)
            ReferralCode.objects.create(partner=partner, referral_code=partner_referral_code, partner_name=partner.name)
        except Exception as e:
            exception_log(e,__file__)
        
    @action(detail=True, methods=['post'], url_path='deactivate', permission_classes=[IsAuthenticated, IsNotBlacklisted, IsAdminUserRole])
    @transaction.atomic
    def deactivate(self, request, pk=None):
        """Deactivate a partner"""
        partner = self.get_object()
        partner.is_active = False
        partner.save(update_fields=['is_active'])
        
        return Response({"info": "PARTNER_DEACTIVATED_SUCCESSFULLY"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='activate', permission_classes=[IsAuthenticated, IsNotBlacklisted, IsAdminUserRole])
    @transaction.atomic
    def activate(self, request, pk=None):
        """Activate a partner"""
        partner = self.get_object()
        partner.is_active = True
        partner.save(update_fields=['is_active'])
        return Response({"info": "PARTNER_ACTIVATED_SUCCESSFULLY"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='change-type', permission_classes=[IsAuthenticated, IsNotBlacklisted, IsAdminUserRole])
    @transaction.atomic
    def change_type(self, request, pk=None):
        """Change the partner type"""
        partner = self.get_object()
        partner_type = request.data.get('partner_type')

        if partner_type not in Partner.PartnerType.values:
            return Response({"info": "INVALID_PARTNER_TYPE"}, status=status.HTTP_400_BAD_REQUEST)

        partner.partner_type = partner_type
        partner.save(update_fields=['partner_type'])
        return Response({"info": "PARTNER_TYPE_UPDATED_SUCCESSFULLY"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='regenerate-referral', permission_classes=[IsAuthenticated, IsNotBlacklisted, IsAdminOrOwner])
    @transaction.atomic
    def regenerate_referral(self, request, pk=None):
        """Regenerate referral code for a partner"""
        partner = self.get_object()
        ReferralCode.objects.filter(partner=partner).update(is_active=False)
        partner_referral_code = generate_referral_code(partner.name)
        ReferralCode.objects.create(partner=partner, referral_code=partner_referral_code, partner_name=partner.name)
        
        return Response({"info": "REFERRAL_CODE_REGENERATED_SUCCESSFULLY", "new_referral_code": new_referral_code}, status=status.HTTP_200_OK)
