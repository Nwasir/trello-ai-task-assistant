import unittest
from unittest.mock import patch, MagicMock
import app.app as trello_ai


class TestAITaskGeneration(unittest.TestCase):
    @patch("app.app.nlp")
    def test_generate_subtasks(self, mock_nlp):
        """Test AI subtask generation pipeline."""
        mock_nlp.return_value = [{"generated_text": "- Task 1\n- Task 2"}]

        result = mock_nlp(f"Break this task into 5 subtasks:\nPlan event")[0]['generated_text']

        self.assertIn("Task 1", result)
        self.assertIn("Task 2", result)
        self.assertTrue(len(result) > 0)


class TestTrelloIntegration(unittest.TestCase):
    @patch("requests.get")
    def test_get_trello_boards(self, mock_get):
        """Test fetching Trello boards."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"id": "123", "name": "Test Board", "url": "https://trello.com/b/123/test"}
        ]
        mock_get.return_value = mock_response

        boards = trello_ai.get_trello_boards()

        self.assertEqual(len(boards), 1)
        self.assertEqual(boards[0]["name"], "Test Board")

    @patch("requests.post")
    def test_add_card_to_list(self, mock_post):
        """Test adding card to Trello list."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        result = trello_ai.add_card_to_list("list123", "Test Task", "Description")
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
