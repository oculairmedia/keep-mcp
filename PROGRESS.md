# Keep MCP Tools Implementation Plan

This document outlines the MCP tools to be implemented for the Google Keep integration.

## Note Management Tools

### `list_notes`
Get all notes with optional filtering by pinned/archived/trashed state.

**Parameters:**
- `pinned` (bool, optional): Filter by pinned status
- `archived` (bool, optional): Filter by archived status
- `trashed` (bool, optional): Filter by trashed status

**Returns:**
- JSON string containing the filtered notes

### `get_note`
Get a specific note by ID.

**Parameters:**
- `note_id` (str): The ID of the note to retrieve

**Returns:**
- JSON string containing the note data

### `search_notes`
Search notes by text content.

**Parameters:**
- `query` (str): The search query

**Returns:**
- JSON string containing the matching notes

### `create_note`
Create a new note with title and text.

**Parameters:**
- `title` (str): The title of the note
- `text` (str): The content of the note
- `pinned` (bool, optional): Whether the note should be pinned (default: False)
- `color` (str, optional): The color of the note

**Returns:**
- JSON string containing the created note's data

### `update_note`
Update a note's properties.

**Parameters:**
- `note_id` (str): The ID of the note to update
- `title` (str, optional): New title for the note
- `text` (str, optional): New text content for the note
- `pinned` (bool, optional): New pinned status
- `color` (str, optional): New color for the note

**Returns:**
- JSON string containing the updated note's data

### `delete_note` ⚠️
Delete a note (mark for deletion).

**Parameters:**
- `note_id` (str): The ID of the note to delete

**Returns:**
- Success message

### `undelete_note`
Undelete a previously deleted note.

**Parameters:**
- `note_id` (str): The ID of the note to undelete

**Returns:**
- JSON string containing the restored note's data

### `trash_note` ⚠️
Move a note to trash.

**Parameters:**
- `note_id` (str): The ID of the note to trash

**Returns:**
- Success message

### `untrash_note`
Restore a note from trash.

**Parameters:**
- `note_id` (str): The ID of the note to untrash

**Returns:**
- JSON string containing the restored note's data

### `archive_note`
Archive a note.

**Parameters:**
- `note_id` (str): The ID of the note to archive

**Returns:**
- Success message

### `unarchive_note`
Unarchive a note.

**Parameters:**
- `note_id` (str): The ID of the note to unarchive

**Returns:**
- Success message

### `pin_note`
Pin a note.

**Parameters:**
- `note_id` (str): The ID of the note to pin

**Returns:**
- Success message

### `unpin_note`
Unpin a note.

**Parameters:**
- `note_id` (str): The ID of the note to unpin

**Returns:**
- Success message

### `change_note_color`
Change a note's color.

**Parameters:**
- `note_id` (str): The ID of the note
- `color` (str): The new color for the note

**Returns:**
- Success message

## List Management Tools

### `list_lists`
Get all list notes.

**Parameters:**
- None

**Returns:**
- JSON string containing all list notes

### `create_list`
Create a new list with title and items.

**Parameters:**
- `title` (str): The title of the list
- `items` (list): List of tuples (text, checked) for each item
- `pinned` (bool, optional): Whether the list should be pinned (default: False)
- `color` (str, optional): The color of the list

**Returns:**
- JSON string containing the created list's data

### `add_list_item`
Add an item to a list.

**Parameters:**
- `note_id` (str): The ID of the list
- `text` (str): The text of the new item
- `checked` (bool, optional): Whether the item is checked (default: False)
- `position` (str, optional): Where to add the item (top, bottom)

**Returns:**
- JSON string containing the updated list's data

### `update_list_item` ⚠️
Update a list item's text or checked status.

**Parameters:**
- `note_id` (str): The ID of the list
- `item_id` (str): The ID of the item to update
- `text` (str, optional): New text for the item
- `checked` (bool, optional): New checked status

**Returns:**
- JSON string containing the updated list's data

### `delete_list_item` ⚠️
Delete a list item.

**Parameters:**
- `note_id` (str): The ID of the list
- `item_id` (str): The ID of the item to delete

**Returns:**
- Success message

### `sort_list`
Sort a list's items.

**Parameters:**
- `note_id` (str): The ID of the list
- `sort_by` (str, optional): How to sort (alphabetical, checked, etc.)

**Returns:**
- JSON string containing the sorted list's data

### `indent_list_item`
Indent a list item.

**Parameters:**
- `note_id` (str): The ID of the list
- `item_id` (str): The ID of the item to indent

**Returns:**
- JSON string containing the updated list's data

### `dedent_list_item`
Dedent a list item.

**Parameters:**
- `note_id` (str): The ID of the list
- `item_id` (str): The ID of the item to dedent

**Returns:**
- JSON string containing the updated list's data

## Label Management Tools

### `list_labels`
Get all labels.

**Parameters:**
- None

**Returns:**
- JSON string containing all labels

### `search_labels`
Search for labels by name.

**Parameters:**
- `query` (str): The search query

**Returns:**
- JSON string containing the matching labels

### `create_label`
Create a new label.

**Parameters:**
- `name` (str): The name of the label

**Returns:**
- JSON string containing the created label's data

### `update_label` ⚠️
Update a label's name.

**Parameters:**
- `label_id` (str): The ID of the label
- `name` (str): The new name for the label

**Returns:**
- JSON string containing the updated label's data

### `delete_label` ⚠️
Delete a label.

**Parameters:**
- `label_id` (str): The ID of the label to delete

**Returns:**
- Success message

### `add_label_to_note`
Add a label to a note.

**Parameters:**
- `note_id` (str): The ID of the note
- `label_id` (str): The ID of the label to add

**Returns:**
- Success message

### `remove_label_from_note`
Remove a label from a note.

**Parameters:**
- `note_id` (str): The ID of the note
- `label_id` (str): The ID of the label to remove

**Returns:**
- Success message

## Media Management Tools

### `list_media`
List all media (images, drawings, audio) in a note.

**Parameters:**
- `note_id` (str): The ID of the note
- `media_type` (str, optional): Type of media to list (image, drawing, audio)

**Returns:**
- JSON string containing the media data

### `get_media_link`
Get a link to download media.

**Parameters:**
- `note_id` (str): The ID of the note
- `media_id` (str): The ID of the media

**Returns:**
- URL string for downloading the media

## Collaboration Tools

### `list_collaborators`
List collaborators for a note.

**Parameters:**
- `note_id` (str): The ID of the note

**Returns:**
- JSON string containing the collaborators' data

### `add_collaborator` ⚠️
Add a collaborator to a note.

**Parameters:**
- `note_id` (str): The ID of the note
- `email` (str): The email of the collaborator to add

**Returns:**
- Success message

### `remove_collaborator` ⚠️
Remove a collaborator from a note.

**Parameters:**
- `note_id` (str): The ID of the note
- `email` (str): The email of the collaborator to remove

**Returns:**
- Success message

## Search and Filter Tools

### `search_by_color`
Search notes by color.

**Parameters:**
- `color` (str): The color to search for

**Returns:**
- JSON string containing the matching notes

### `search_by_label`
Search notes by label.

**Parameters:**
- `label_id` (str): The ID of the label to search for

**Returns:**
- JSON string containing the matching notes

### `search_by_date`
Search notes by creation/update date.

**Parameters:**
- `start_date` (str, optional): Start date in ISO format
- `end_date` (str, optional): End date in ISO format
- `date_field` (str, optional): Which date field to use (created, updated, edited)

**Returns:**
- JSON string containing the matching notes 