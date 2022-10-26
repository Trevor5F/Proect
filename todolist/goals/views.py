from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions, filters

from goals.filters import GoalDateFilter
from goals.models import GoalCategory, Goal
from goals.serializer import GoalCategoryCreateSerializer, GoalCategorySerializer, GoalCreateSerializer, GoalSerializer, \
    GoalCommentCreateSerializer, GoalComment, GoalCommentSerializer


class GoalCategoryCreateView(CreateAPIView):
    serializer_class = GoalCategoryCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class GoalCategoryListView(ListAPIView):
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategorySerializer
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]

    def get_queryset(self):
        return GoalCategory.objects.filter(user=self.request.user, is_deleted=False)


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return GoalCategory.objects.filter(user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance: GoalCategory):
        instance.is_deleted = True
        instance.save()
        return instance



class GoalCreateView(CreateAPIView):
    serializer_class = GoalCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class GoalListView(ListAPIView):
    model = Goal
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalSerializer
    filterset_class = GoalDateFilter
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title", "description"]

    def get_queryset(self):
        return Goal.objects.filter(Q(user_id=self.request.user.id) & ~Q(status=Goal.Status.archived))


class GoalView(RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Goal.objects.filter(Q(user_id=self.request.user.id) & ~Q(status=Goal.Status.archived))



class GoalCommentCreateView(CreateAPIView):
    serializer_class = GoalCommentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class GoalCommentListView(ListAPIView):
    model = GoalComment
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCommentSerializer
    filter_backends = [OrderingFilter]
    filterset_fields = ['goal']
    ordering = ["-created"]


    def get_queryset(self):
        return GoalComment.objects.filter(user_id=self.request.user.id)


class GoalCommentView(RetrieveUpdateDestroyAPIView):
    model = GoalComment
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCommentSerializer

    def get_queryset(self):
        return GoalComment.objects.filter(user_id=self.request.user.id)

