import json
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse


class TestChatsEndpoints(TestCase):

	def test_test_endpoint_returns_server_message(self):
		response = self.client.get(reverse("test"))

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.content.decode(), "Rem Backend Server is running")

	@patch("chats.views.generate_reply")
	def test_chat_endpoint_returns_generated_reply(self, mock_generate_reply):
		mock_generate_reply.return_value = "Hi there"

		response = self.client.post(
			reverse("chat"),
			data=json.dumps({"message": "Hello"}),
			content_type="application/json",
		)

		self.assertEqual(response.status_code, 200)
		self.assertJSONEqual(response.content, {"reply": "Hi there"})
		mock_generate_reply.assert_called_once_with("Hello")
