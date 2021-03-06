from rest_framework.views import APIView
from rest_framework.response import Response
from . import models, serializers
from khangram.notifications import views as notification_views
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView


class ExploreUsers(APIView):

    def get(self, request, format=None):

        last_five = models.User.objects.all().order_by('date_joined')[:5]

        serializer = serializers.ListUserSerializer(last_five, many=True, context={"request": request})

        return Response(data=serializer.data, status=200)


class FollowUser(APIView):

    def post(self, request, user_id, format=None):

        user = request.user

        try:
            user_to_follow = models.User.objects.get(id=user_id)
        except models.User.DoesNotExist:
            return Response(status=404)

        user.following.add(user_to_follow)

        user.save()

        notification_views.create_notification(user, user_to_follow, 'follow')

        return Response(status=200)

class UnFollowUser(APIView):

    def post(self, request, user_id, format=None):

        user = request.user
        try:
            uset_to_follow = models.User.objects.get(id=user_id)
        except models.User.DoesNotExist:
            return Response(status=404)

        user.following.remove(user_to_follow)

        user.save()

        return Response(status=200)


class UserProfile(APIView):

    def get_user(self, username):

        try:
            found_user = models.User.objects.get(username=username)
            return found_user
        except models.User.DoesNotExist:
            return None


    def get(self, request, username, format=None):

        found_user=self.get_user(username)

        if found_user is None:

            return Response(status=404)

        serializer = serializers.UserProfilesSerializer(found_user)

        return Response(data=serializer.data, status=200)

    def put(self, request, username, format=None):

        user = request.user

        found_user = self.get_user(username)

        if found_user is None:

            return Response(status=404)
        
        elif found_user.username != user.username:

            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        else:

            serializer = serializers.UserProfilesSerializer(
                found_user, data=request.data, partial=True)

            if serializer.is_valid():

                serializer.save()

                return Response(data=serializer.data, status=200)

            else:

                return Response(data=serializer.errors, status=400)




class UserFollowers(APIView):

    def get(self, request, username, format=None):

        try:
            found_user = models.User.objects.get(username=username)
        except models.User.DoesNotExist:
            return Response(status=200)
        
        user_followers = found_user.followers.all()

        serializer = serializers.ListUserSerializer(user_followers, many=True, context={"request": request})

        return Response(data=serializer.data, status=200)


class UserFollowing(APIView):

    def get(self, request, username, format=None):

        try:
            found_user = models.User.objects.get(username=username)
        except models.User.DoesNotExist:
            return Response(status=200)
        
        user_following = found_user.following.all()

        serializer = serializers.ListUserSerializer(user_following, many=True, context={"request": request})

        return Response(data=serializer.data, status=200)


class Search(APIView):

    def get(self, request, format=None):

        username = request.query_params.get('username', None)

        if username is not None:

            users = models.User.objects.filter(username__istartwith=username)

            serializer = serializers.ListUserSerializer(users, many=True, context={"request": request})

            return Response(data=serializer.data, status=200)

        else:

            return Response(status=400)


class ChangePassword(APIView):

    def put(self, request, username, format=None):

        user = request.user

        if user.username == username:

            current_password = request.data.get('current_password', None)

            if current_password is not None:

                password_match = user.check_password(current_password)

                if password_match:

                    new_password = request.data.get('new_password', None)

                    if new_password is not None:

                        user.set_password(new_password)

                        user.save()

                        return Response(status=200)

                    else:

                        return Response(status=400)

                else:

                    return Response(status=400)

            else:

                return Response(status=400)

        else:

            return Response(status=status.HTTP_400_BAD_REQUEST)


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter