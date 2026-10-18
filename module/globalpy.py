
class GlobalVar():
    json_data = {
        "sent_template_message_id" : "",
        "sent_template_channel_id" : "",

        
        "check_result_message_id": "",

        # 0 - not done for the month
        # 1 - done for the month
        # Default to not done
        "black_mage_done": "0",
        
        # tell me which month done/not done
        # default to "Current Month"
        "black_mage_month": "Current Month",
    }

    JSON_FILE_PATH = './generated/data.json'