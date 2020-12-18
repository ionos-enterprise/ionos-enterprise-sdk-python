import ionoscloud
from coreadaptor.IonosCoreProxy import IonosCoreProxy


class image:

    @IonosCoreProxy.process_response
    def get_image(self, image_id):
        """
        Retrieves a single image by ID.

        :param      image_id: The unique ID of the image.
        :type       image_id: ``str``

        """
        return self.get_api_instance(ionoscloud.ImageApi)\
            .images_find_by_id_with_http_info(image_id, response_type='object')

    @IonosCoreProxy.process_response
    def list_images(self, depth=1):
        """
        Retrieves a list of images available in the data center.

        :param      depth: The depth of the response data.
        :type       depth: ``int``
        """
        return self.get_api_instance(ionoscloud.ImageApi)\
            .images_get_with_http_info(depth=depth, response_type='object')

    @IonosCoreProxy.process_response
    def delete_image(self, image_id):
        """
        Removes only user created images.

        :param      image_id: The unique ID of the image.
        :type       image_id: ``str``

        """
        return self.get_api_instance(ionoscloud.ImageApi).images_delete_with_http_info(image_id)

    @IonosCoreProxy.process_response
    def update_image(self, image_id, **kwargs):
        """
        Replace all properties of an image.

        """
        data = {}

        for attr, value in kwargs.items():
            data[self._underscore_to_camelcase(attr)] = value

        image = ionoscloud.models.Image(
            properties=data
        )

        return self.get_api_instance(ionoscloud.ImageApi)\
            .images_patch_with_http_info(image_id, image, response_type='object')
