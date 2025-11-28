import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def extract_text_messages_until_timestamp(
    driver, until_timestamp, max_scroll_attempts=50
):
    """
    Scroll from the latest message upward and extract text messages
    (including those with media) until the given timestamp.
    """

    messages_data = []
    seen_message_ids = set()
    scroll_attempts = 0

    try:
        # Find the main chat container
        chat_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".scrollable.scrollable-y")
            )
        )

        ########################################
        print(chat_container)
        ########################################

        # Scroll to the bottom (latest message)
        driver.execute_script(
            "arguments[0].scrollTop = arguments[0].scrollHeight", chat_container
        )
        time.sleep(2)

        last_height = driver.execute_script(
            "return arguments[0].scrollHeight", chat_container
        )

        while scroll_attempts < max_scroll_attempts:
            # Find all messages (excluding date separators)
            message_elements = chat_container.find_elements(
                By.CSS_SELECTOR, ".bubble:not(.is-date)"
            )

            new_messages_found = False

            # Process messages from newest to oldest
            for message in reversed(message_elements):
                try:
                    message_info = extract_single_message_info(driver, message)

                    # Skip invalid or already seen messages
                    if (
                        not message_info
                        or message_info["message_id"] in seen_message_ids
                    ):
                        continue

                    message_timestamp = int(message_info["timestamp"])

                    # Stop if reached target timestamp
                    if message_timestamp <= until_timestamp:
                        print(
                            "Reached target timestamp. Stopping message extraction..."
                        )
                        break

                    # Add message to results
                    seen_message_ids.add(message_info["message_id"])
                    messages_data.append(message_info)
                    new_messages_found = True

                    print(
                        f"New message ({message_info['type']}): {message_info['time']} - {message_info['text'][:50]}..."
                    )

                except Exception as e:
                    print(f"Error processing message: {e}")
                    continue

            # Stop if no new messages found
            if not new_messages_found:
                print("No new messages found. Stopping...")
                break

            # Scroll upward to load older messages
            driver.execute_script(
                """
                var container = arguments[0];
                container.scrollTop = container.scrollTop - container.clientHeight * 2;
                """,
                chat_container,
            )

            time.sleep(2)

            # Check scroll position and height
            new_height = driver.execute_script(
                "return arguments[0].scrollHeight", chat_container
            )
            current_scroll = driver.execute_script(
                "return arguments[0].scrollTop", chat_container
            )

            if current_scroll <= 0 or new_height == last_height:
                print("Reached the top of the chat. Stopping...")
                break

            last_height = new_height
            scroll_attempts += 1
            print(
                f"Scroll attempt {scroll_attempts}. Messages extracted so far: {len(messages_data)}"
            )

    except Exception as e:
        print(f"Error during scrolling process: {e}")

    # Sort messages from oldest to newest
    messages_data.sort(key=lambda x: int(x["timestamp"]))

    return messages_data


def extract_single_message_info(driver, message_element):
    """
    Extract information from a single message element (supports text, media, reply, etc.)
    """

    try:
        # Extract IDs
        message_id = message_element.get_attribute("data-mid")
        peer_id = message_element.get_attribute("data-peer-id")
        timestamp = message_element.get_attribute("data-timestamp")

        if not message_id or not timestamp:
            return None

        # Extract text content
        text_content = ""
        message_text_element = message_element.find_elements(
            By.CSS_SELECTOR, ".message"
        )
        if message_text_element:
            text_content = driver.execute_script(
                """
                var messageElement = arguments[0];
                var clone = messageElement.cloneNode(true);
                var timeElements = clone.querySelectorAll('.time');
                timeElements.forEach(function(timeElement) {
                    if (timeElement.parentNode) {
                        timeElement.parentNode.removeChild(timeElement);
                    }
                });
                return clone.textContent.trim();
                """,
                message_text_element[0],
            )

        # Detect media
        message_type = "text"
        media_info = {}
        media_element = message_element.find_elements(
            By.CSS_SELECTOR, ".attachment.media-container"
        )
        if media_element:
            img_element = media_element[0].find_elements(
                By.CSS_SELECTOR, "img.media-photo"
            )
            if img_element:
                src = img_element[0].get_attribute("src")
                if "google.com/vt/lyrs=m" in src:
                    message_type = "map"
                    media_info = {"type": "map", "src": src}
                else:
                    message_type = "image"
                    media_info = {"type": "image", "src": src}
            else:
                message_type = "media"
                media_info = {"type": "unknown"}

        # Extract reply info
        reply_info = {}
        reply_element = message_element.find_elements(By.CSS_SELECTOR, ".reply")
        if reply_element:
            try:
                reply_title = (
                    reply_element[0].find_element(By.CSS_SELECTOR, ".reply-title").text
                )
                reply_subtitle = (
                    reply_element[0]
                    .find_element(By.CSS_SELECTOR, ".reply-subtitle")
                    .text
                )
                reply_info = {"title": reply_title, "subtitle": reply_subtitle}
                if text_content:
                    text_content += f" [Reply to: {reply_title} - {reply_subtitle}]"
            except Exception as e:
                print(f"Error extracting reply info: {e}")

        if not text_content and not media_info:
            return None

        # Extract time
        time_element = message_element.find_element(By.CSS_SELECTOR, ".time")
        message_time = (
            time_element.get_attribute("title")
            if time_element.get_attribute("title")
            else time_element.text
        )

        # Status
        status = "sent"
        if "is-read" in message_element.get_attribute("class"):
            status = "read"
        elif "is-delivered" in message_element.get_attribute("class"):
            status = "delivered"

        # Direction
        direction = (
            "outgoing"
            if "is-out" in message_element.get_attribute("class")
            else "incoming"
        )

        # Sender name
        sender_name = ""
        name_element = message_element.find_elements(By.CSS_SELECTOR, ".name")
        if name_element:
            try:
                sender_name = (
                    name_element[0].find_element(By.CSS_SELECTOR, ".peer-title").text
                )
            except:
                sender_name = name_element[0].text

        if not sender_name and direction == "incoming":
            try:
                avatar_element = message_element.find_element(
                    By.CSS_SELECTOR, ".user-avatar .avatar-photo"
                )
                sender_name = f"User_{peer_id}"
            except:
                pass

        if not sender_name and direction == "outgoing":
            sender_name = "You"

        return {
            "message_id": message_id,
            "peer_id": peer_id,
            "timestamp": timestamp,
            "time": message_time,
            "text": text_content,
            "sender": sender_name,
            "status": status,
            "direction": direction,
            "type": message_type,
            "has_media": bool(media_info),
            "media_info": media_info,
            "has_reply": bool(reply_info),
            "reply_info": reply_info,
        }

    except Exception as e:
        print(f"Error extracting message info: {e}")
        try:
            html_content = message_element.get_attribute("outerHTML")
            print(f"Problematic element HTML: {html_content[:500]}...")
        except:
            pass
        return None
