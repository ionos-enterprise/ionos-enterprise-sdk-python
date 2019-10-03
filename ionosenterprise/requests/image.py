import json


class image:
    def get_image(self, image_id):
        """
        Retrieves a single image by ID.

        :param      image_id: The unique ID of the image.
        :type       image_id: ``str``

        """
        response = self._perform_request('/images/%s' % image_id)
        return response

    def list_images(self, depth=1):
        """
        Retrieves a list of images available in the data center.

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        response = self._perform_request('/images?depth=' + str(depth))
        return response

    def delete_image(self, image_id):
        """
        Removes only user created images.

        :param      image_id: The unique ID of the image.
        :type       image_id: ``str``

        """
        response = self._perform_request(url='/images/' + image_id,
                                         method='DELETE')
        return response

    def update_image(self, image_id, **kwargs):
        """
        Replace all properties of an image.

        """
        data = {}

        for attr, value in kwargs.items():
            data[self._underscore_to_camelcase(attr)] = value

        response = self._perform_request(url='/images/' + image_id,
                                         method='PATCH',
                                         data=json.dumps(data))
        return response
