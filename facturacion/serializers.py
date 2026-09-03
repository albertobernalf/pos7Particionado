from rest_framework import serializers

class FacturaDianSerializer(serializers.Serializer):
    nit_emisor = serializers.CharField(max_length=20)
    xml_base64 = serializers.CharField()

    def validate_xml_base64(self, value):
        # Aquí puedes agregar validaciones personalizadas, 
        # por ejemplo, verificar si el string contiene una cabecera Base64 válida.
        return value

    def validate(self, data):
        # Validación a nivel de todo el objeto
        return data