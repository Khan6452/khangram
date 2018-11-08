from rest_framework.views import APIView
from rest_framework.response import Response
from . import models, serializers
from khangram.users import models as user_models
from khangram.users import serializers as user_serializers
from khangram.notifications import views as notificaion_views
from rest_framework import status


class Images(APIView):
    
    def get(self, request, format=None):

        user = request.user

        following_users = user.following.all()

        image_list = []

        for following_user in following_users:

            user_images = following_user.images.all()[:2]

            for image in user_images:

                image_list.append(image)

        my_images = user.images.all()[:2]

        for image in my_images:

            image_list.append(image)

        sorted_list = sorted(image_list, key=lambda image: image.created_at, reverse=True)

        serializer = serializers.ImageSerializer(sorted_list, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):

        user = request.user

        serializer = serializers.InputImageSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save(creator=user)

            return Response(data=serializer.data, status=200)


        else:
            return Response(data=serializer.errors, status=400)


class LikeImage(APIView):

    def get(self, request, image_id, format=None):

        likes = models.Like.objects.filter(image__id=image_id)

        like_creators_ids = likes.values('creator_id')

        users = user_models.User.objects.filter(id__in=like_creators_ids)

        serializer = user_serializers.ListUserSerializer(users, many=True, context={"request" : request})

        return Response(data=serializer.data, status=200)


    def post(self, request, image_id, format=None):

        user = request.user

        try:
            found_image = models.Image.objects.get(id=image_id)
        except models.Image.DoesNotExist:
            return Response(status=404)

        try:
            preexisting_like = models.Like.objects.get(
                creator=user,
                image=found_image
            )
            return Response(status=204)

        except models.Like.DoesNotExist:
            
            new_like = models.Like.objects.create(
                creator=user,
                image=found_image
            )

            notificaion_views.create_notification(
                user, found_image.creator, 'like', found_image )

            new_like.save()

        return Response(status=200)


class UnLikeImage(APIView):

    def delete(self, request, image_id, format=None):

        user = request.user

        try:
            found_image = models.Image.objects.get(id=image_id)
        except models.Image.DoesNotExist:
            return Response(status=404)

        try:
            preexisting_like = models.Like.objects.get(
                creator=user,
                image=found_image
            )
            preexisting_like.delete()

            return Response(status=204)
 
        except models.Like.DoesNotExist:

            return Response(status=304)



class CommentOnImage(APIView):

    def post(self, request, image_id, format=None):

        user = request.user

        try:
            found_image = models.Image.objects.get(id=image_id)
        except models.Image.DoesNotExist:
            return Response(status=404)

        serializer = serializers.CommentSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save(creator=user, image=found_image)

            notificaion_views.create_notification(
                user, found_image.creator, 'comment', found_image, serializer.data['message'])

            return Response(data=serializer.data, status=201)

        else:

            return Response(data=serializer.errors, status=400)


class Comment(APIView):

    def delete(self, request, comment_id, format=None):

        user = request.user

        try:
            comment = models.Comment.objects.get(id=comment_id, creator=user)
            comment.delete()
            return Response(status=202)
        except models.Comment.DoesNotExist:
            return Response(status=404)


class Search(APIView):

    def get(self, request, format=None):

        hashtags = request.query_params.get('hashtags', None)

        if hashtags is not None:

            hashtags = hashtags.split(",")

            images = models.Image.objects.filter(tags__name__in=hashtags).distinct()

            serializer = serializers.UserProfileImageSerializer(images, many=True, context={"request": request})

            return Response(data=serializer.data, status=200)

        else:

            return response(status=404)


class ModerateComments(APIView):

    def delete(self, request, image_id, comment_id, format=None):

        user = request.user

        try:
            comment_to_delete = models.Comment.objects.get(
                id=comment_id, image__id=image_id, image__creator=user)
            comment_to_delete.delete()
        except models.Comment.DoesNotExist:
            return Response(status=404)

        return Response(status=204)



class ImageDetail(APIView):

    def find_own_image(self, image_id, user):
        try:
            image = models.Image.objects.get(id=image_id, creator=user)
            return image
        except models.Image.DoesNotExist:
            return None

    def get(self, request, image_id, format=None):

        user = request.user

        try:
            image = models.Image.objects.get(id=image_id)
        except models.Image.DoesNotExist:
            return Response(status=404)

        serializer = serializers.ImageSerializer(image, context={'request': request})

        return Response(data=serializer.data, status=200)


    def put(self, request, image_id, format=None):

        user= request.user

        image = self.find_own_image(image_id, user)

        if image is None:

            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.InputImageSerializer(image, data=request.data, partial=True)

        if serializer.is_valid():

            serializer.save(creator=user)

            return Response(data=serializer.data, status=204)

        else:

            return Response(data=serializer.data, status=400)

    def delete(self, request, image_id, format=None):

        user = request.user

        image = self.find_own_image(image_id, user)

        if image is None:

            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        image.delete()

        return Response(status=204)




#----------------------------------------------------------
# Create your views here.

#def get_key(image):
#    return image.created_at

#class ListAllImages(APIView):
#
#    def get(self, request, format=None):
#
#        all_images = models.Image.objects.all()
#
#        serializer = serializers.ImageSerializer(all_images, many=True)
#
#        return Response(data=serializer.data)


#class ListAllComments(APIView):
#
#    def get(self, request, format=None):
#
#        all_comments = models.Comment.objects.all()
#
#        serializer = serializers.CommentSerializer(all_comments, many=True)
#
#        return Response(data=serializer.data)


#class ListAllLikes(APIView):
#
#    def get(self, request, format=None):
#
#        all_Likes = models.Like.objects.all()
#
#        serializer = serializers.LikeSerializer(all_Likes, many=True)
#
#        return Response(data=serializer.data)