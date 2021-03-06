from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView

from track.models import Bogger, CalorieEntry, DailyEntry, Goal
from track.serializers import UserSerializer, BoggerSerializer, CalorieEntrySerializer, DailyEntrySerializer, \
        GoalSerializer
from track.permissions import IsOwnerOrStaff


class CalorieEntryViewSet(viewsets.ModelViewSet):
    serializer_class = CalorieEntrySerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrStaff,)
    queryset = CalorieEntry.objects.all()

    def get_queryset(self):
        return CalorieEntry.objects.filter(bogger__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(bogger=self.request.user.bogger)


class DailyEntryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DailyEntrySerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrStaff,)
    queryset = DailyEntry.objects.all()
    lookup_field = 'date'
    lookup_value_regex = '[0-9]{4}-[0-9]{2}-[0-9]{2}'

    def get_queryset(self):
        return DailyEntry.objects.filter(bogger__user=self.request.user)


class GoalViewSet(viewsets.ModelViewSet):
    serializer_class = GoalSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrStaff,)
    queryset = Goal.objects.all()
    lookup_field = 'date'
    lookup_value_regex = '[0-9]{4}-[0-9]{2}-[0-9]{2}'

    def get_queryset(self):
        return Goal.objects.filter(bogger__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(bogger=self.request.user.bogger)


class BoggerView(RetrieveUpdateAPIView):
    """
    API endpoint that allows a user to be viewed or edited.
    """
    serializer_class = BoggerSerializer
    queryset = Bogger.objects.all()

    def get_object(self):
        pk = self.kwargs.get('pk', None)
        if not pk or (pk == str(self.request.user.pk)):
            return self.request.user.bogger
        else:
            try:
                return get_object_or_404(User, id=pk)
            except ValueError:
                return get_object_or_404(User, username=pk)


class CreateBoggerView(CreateAPIView):
    """
    API endpoint that allows a user to be viewed or edited.
    """
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    queryset = User.objects.all()
