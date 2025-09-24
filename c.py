import socket
import threading
import time
import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from protobuf_decoder.protobuf_decoder import Parser
import json

class GamePacketHandler:
    def __init__(self):
        # Encryption settings
        self.key = b'Yg&tc%DEuh6%Zc^8'
        self.iv = b'6oyZDr22E3ychjM%'
        self.socket_client = None
        self.is_spamming = False
        
        # Constants
        self.dec = ['80', '81', '82', '83', '84', '85', '86', '87', '88', '89', 
                   '8a', '8b', '8c', '8d', '8e', '8f', '90', '91', '92', '93', 
                   '94', '95', '96', '97', '98', '99', '9a', '9b', '9c', '9d', 
                   '9e', '9f', 'a0', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 
                   'a8', 'a9', 'aa', 'ab', 'ac', 'ad', 'ae', 'af', 'b0', 'b1', 
                   'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'ba', 'bb', 
                   'bc', 'bd', 'be', 'bf', 'c0', 'c1', 'c2', 'c3', 'c4', 'c5', 
                   'c6', 'c7', 'c8', 'c9', 'ca', 'cb', 'cc', 'cd', 'ce', 'cf', 
                   'd0', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 
                   'da', 'db', 'dc', 'dd', 'de', 'df', 'e0', 'e1', 'e2', 'e3', 
                   'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'ea', 'eb', 'ec', 'ed', 
                   'ee', 'ef', 'f0', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 
                   'f8', 'f9', 'fa', 'fb', 'fc', 'fd', 'fe', 'ff']
        
        self.x = ['1','01', '02', '03', '04', '05', '06', '07', '08', '09', 
                 '0a', '0b', '0c', '0d', '0e', '0f', '10', '11', '12', '13', 
                 '14', '15', '16', '17', '18', '19', '1a', '1b', '1c', '1d', 
                 '1e', '1f', '20', '21', '22', '23', '24', '25', '26', '27', 
                 '28', '29', '2a', '2b', '2c', '2d', '2e', '2f', '30', '31', 
                 '32', '33', '34', '35', '36', '37', '38', '39', '3a', '3b', 
                 '3c', '3d', '3e', '3f', '40', '41', '42', '43', '44', '45', 
                 '46', '47', '48', '49', '4a', '4b', '4c', '4d', '4e', '4f', 
                 '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', 
                 '5a', '5b', '5c', '5d', '5e', '5f', '60', '61', '62', '63', 
                 '64', '65', '66', '67', '68', '69', '6a', '6b', '6c', '6d', 
                 '6e', '6f', '70', '71', '72', '73', '74', '75', '76', '77', 
                 '78', '79', '7a', '7b', '7c', '7d', '7e', '7f']
        
        self.avatar_list = [
            902000061, 902000060, 902000064, 902000065, 902000066,
            902000074, 902000075, 902000077, 902000078, 902000084,
            902000085, 902000087, 902000091, 902000094, 902000306,
            902000004, 902000001, 902000006, 902000003, 902000055,
            902000208, 902000209, 902000210, 902000211
        ]
        
        self.color_list = [
            "[00FF00][b][c]", "[FFDD00][b][c]", "[3813F3][b][c]", 
            "[FF0000][b][c]", "[0000FF][b][c]", "[FFA500][b][c]",
            "[DF07F8][b][c]", "[11EAFD][b][c]", "[DCE775][b][c]",
            "[A8E6CF][b][c]", "[7CB342][b][c]", "[FF0000][b][c]",
            "[FFB300][b][c]", "[90EE90][b][c]"
        ]

    # Encryption/Decryption Methods
    def encrypt_packet(self, plain_text):
        """Encrypt packet using AES-CBC"""
        plain_text = bytes.fromhex(plain_text)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        cipher_text = cipher.encrypt(pad(plain_text, AES.block_size))
        return cipher_text.hex()

    def decrypt_packet(self, cipher_text):
        """Decrypt packet using AES-CBC"""
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        plain_text = unpad(cipher.decrypt(bytes.fromhex(cipher_text)), AES.block_size)
        return plain_text.hex()

    # Utility Methods
    def dec_to_hex(self, decimal):
        """Convert decimal to hexadecimal string"""
        hex_str = hex(decimal)[2:]
        return hex_str.zfill(2) if len(hex_str) == 1 else hex_str

    def get_random_avatar(self):
        """Get a random avatar ID"""
        return random.choice(self.avatar_list)

    def generate_random_color(self):
        """Generate a random color tag"""
        return random.choice(self.color_list)

    def generate_random_hex_color(self):
        """Generate random hex color code"""
        top_colors = [
            "FF4500", "FFD700", "32CD32", "87CEEB", "9370DB",
            "FF69B4", "8A2BE2", "00BFFF", "1E90FF", "20B2AA",
            "00FA9A", "008000", "FFFF00", "FF8C00", "DC143C",
            "FF6347", "FFA07A", "FFDAB9", "CD853F", "D2691E",
            "BC8F8F", "F0E68C", "556B2F", "808000", "4682B4",
            "6A5ACD", "7B68EE", "8B4513", "C71585", "4B0082",
            "B22222", "228B22", "8B008B", "483D8B", "556B2F",
            "800000", "008080", "000080", "800080", "808080",
            "A9A9A9", "D3D3D3", "F0F0F0"
        ]
        return random.choice(top_colors)

    # Protobuf Packet Handling
    def create_protobuf_packet(self, fields):
        """Create protobuf packet from dictionary of fields"""
        packet = bytearray()
        
        for field, value in fields.items():
            if isinstance(value, dict):
                nested_packet = self.create_protobuf_packet(value)
                packet.extend(self.create_length_delimited_field(field, nested_packet))
            elif isinstance(value, int):
                packet.extend(self.create_varint_field(field, value))
            elif isinstance(value, str) or isinstance(value, bytes):
                packet.extend(self.create_length_delimited_field(field, value))
        
        return packet

    def create_varint_field(self, field_number, value):
        """Create varint field"""
        field_header = (field_number << 3) | 0  # Varint wire type is 0
        return self.encode_varint(field_header) + self.encode_varint(value)

    def create_length_delimited_field(self, field_number, value):
        """Create length-delimited field"""
        field_header = (field_number << 3) | 2  # Length-delimited wire type is 2
        encoded_value = value.encode() if isinstance(value, str) else value
        return self.encode_varint(field_header) + self.encode_varint(len(encoded_value)) + encoded_value

    def encode_varint(self, number):
        """Encode number as varint"""
        if number < 0:
            raise ValueError("Number must be non-negative")

        encoded_bytes = []
        while True:
            byte = number & 0x7F
            number >>= 7
            if number:
                byte |= 0x80
            encoded_bytes.append(byte)
            if not number:
                break
        return bytes(encoded_bytes)

    # Room Spamming Functionality
    def spam_room(self, room_id, player_id):
        """Create spam packet for room"""
        fields = {
            1: 78,
            2: {
                1: int(room_id),
                2: "[FF0000]بوت تيم قواقزه ZIX",
                4: 330,
                5: 6000,
                6: 201,
                10: int(self.get_random_avatar()),
                11: int(player_id),
                12: 1
            }
        }
        
        packet = self.create_protobuf_packet(fields).hex()
        encrypted_packet = self.encrypt_packet(packet)
        header_length = len(encrypted_packet) // 2
        header_length_hex = self.dec_to_hex(header_length)
        
        # Format final packet based on header length
        if len(header_length_hex) == 2:
            final_packet = "0E15000000" + header_length_hex + encrypted_packet
        elif len(header_length_hex) == 3:
            final_packet = "0E1500000" + header_length_hex + encrypted_packet
        elif len(header_length_hex) == 4:
            final_packet = "0E150000" + header_length_hex + encrypted_packet
        elif len(header_length_hex) == 5:
            final_packet = "0E15000" + header_length_hex + encrypted_packet
            
        return bytes.fromhex(final_packet)

    # Network Operations
    def connect_to_server(self, host, port):
        """Connect to game server"""
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_client.connect((host, port))
        print(f"Connected to {host}:{port}")

    def start_spam(self, room_id, player_id, count=100, delay=1):
        """Start spamming a room"""
        if not self.socket_client:
            print("Not connected to server!")
            return
            
        self.is_spamming = True
        spam_packet = self.spam_room(room_id, player_id)
        
        for i in range(count):
            if not self.is_spamming:
                break
                
            try:
                self.socket_client.send(spam_packet)
                print(f"Sent spam packet {i+1}/{count}")
                time.sleep(delay)
            except Exception as e:
                print(f"Error sending packet: {e}")
                break
                
        self.is_spamming = False

    def stop_spam(self):
        """Stop spamming"""
        self.is_spamming = False

    # Additional Packet Types
    def send_message(self, message, room_id=None):
        """Send message to room or player"""
        fields = {
            1: 1,
            2: {
                1: 9280892890,
                2: 3045484556 if room_id is None else int(room_id),
                3: 1 if room_id is None else 3,
                4: f'[{self.generate_random_hex_color()}]{message}',
                5: 1721662811,
                7: 2,
                9: {
                    1: "byte bot ",
                    2: self.get_random_avatar(),
                    4: 228,
                    7: 1,
                },
                10: "en",
                13: {
                    2: 1,
                    3: 1
                },
            }
        }
        
        packet = self.create_protobuf_packet(fields).hex() + "7200"
        return self._format_packet(packet, "1215")

    def join_room(self, room_id):
        """Create join room packet"""
        fields = {
            1: 3,
            2: {
                1: int(room_id),
                2: "ME",
                4: 1,
            }
        }
        
        packet = self.create_protobuf_packet(fields).hex()
        return self._format_packet(packet, "0515")

    def _format_packet(self, packet, prefix):
        """Format packet with appropriate header"""
        encrypted_packet = self.encrypt_packet(packet)
        header_length = len(encrypted_packet) // 2
        header_length_hex = self.dec_to_hex(header_length)
        
        if len(header_length_hex) == 2:
            final_packet = prefix + "000000" + header_length_hex + encrypted_packet
        elif len(header_length_hex) == 3:
            final_packet = prefix + "00000" + header_length_hex + encrypted_packet
        elif len(header_length_hex) == 4:
            final_packet = prefix + "0000" + header_length_hex + encrypted_packet
        elif len(header_length_hex) == 5:
            final_packet = prefix + "000" + header_length_hex + encrypted_packet
            
        return bytes.fromhex(final_packet)

    # Packet Analysis
    def parse_packet(self, packet):
        """Parse protobuf packet"""
        try:
            parsed_results = Parser().parse(packet)
            parsed_results_dict = self._parse_results(parsed_results)
            return json.dumps(parsed_results_dict, indent=2)
        except Exception as e:
            print(f"Error parsing packet: {e}")
            return None

    def _parse_results(self, parsed_results):
        """Convert parsed results to dictionary"""
        result_dict = {}
        for result in parsed_results:
            field_data = {'wire_type': result.wire_type}
            
            if result.wire_type == "varint":
                field_data['data'] = result.data
            elif result.wire_type in ["string", "bytes"]:
                field_data['data'] = result.data
            elif result.wire_type == 'length_delimited':
                field_data['data'] = self._parse_results(result.data.results)
                
            result_dict[result.field] = field_data
        return result_dict


# Example usage with Telegram bot
# Example usage with Telegram bot
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

class TelegramBotHandler:
    def __init__(self, token, packet_handler):
        self.updater = Updater(token)  # تم إزالة use_context هنا
        self.dp = self.updater.dispatcher
        self.packet_handler = packet_handler
        
        # Add command handlers
        self.dp.add_handler(CommandHandler("start", self.start))
        self.dp.add_handler(CommandHandler("spam_room", self.spam_room))
        self.dp.add_handler(CommandHandler("stop_spam", self.stop_spam))
        self.dp.add_handler(CommandHandler("send_message", self.send_message))
        self.dp.add_handler(CommandHandler("join_room", self.join_room))

    def start(self, update: Update, context: CallbackContext):
        """Send welcome message"""
        update.message.reply_text(
            "مرحباً بكم في بوت إدارة الروم! الأوامر المتاحة:\n"
            "/spam_room [room_id] [player_id] [count]\n"
            "/stop_spam\n"
            "/send_message [message] [room_id]\n"
            "/join_room [room_id]"
        )

    def spam_room(self, update: Update, context: CallbackContext):
        """Handle spam_room command"""
        if len(context.args) < 2:
            update.message.reply_text("استخدم: /spam_room [room_id] [player_id] [count=100]")
            return
        
        room_id = context.args[0]
        player_id = context.args[1]
        count = int(context.args[2]) if len(context.args) > 2 else 100
        
        # Connect to server (replace with actual server details)
        self.packet_handler.connect_to_server("98.98.162.80", 39698)
        
        # Start spamming in separate thread
        spam_thread = threading.Thread(
            target=self.packet_handler.start_spam,
            args=(room_id, player_id, count)
        )
        spam_thread.start()
        
        update.message.reply_text(f"بدأ سبام الروم {room_id} للاعب {player_id} ({count} مرة)")

    def stop_spam(self, update: Update, context: CallbackContext):
        """Handle stop_spam command"""
        self.packet_handler.stop_spam()
        update.message.reply_text("تم إيقاف السبام")

    def send_message(self, update: Update, context: CallbackContext):
        """Handle send_message command"""
        if len(context.args) < 1:
            update.message.reply_text("استخدم: /send_message [message] [room_id]")
            return
            
        message = " ".join(context.args[:-1]) if len(context.args) > 1 else context.args[0]
        room_id = context.args[-1] if len(context.args) > 1 else None
        
        # Connect to server if not already connected
        if not self.packet_handler.socket_client:
            self.packet_handler.connect_to_server("98.98.162.80", 39698)
            
        packet = self.packet_handler.send_message(message, room_id)
        try:
            self.packet_handler.socket_client.send(packet)
            update.message.reply_text(f"تم إرسال الرسالة إلى {'الروم' if room_id else 'اللاعب'}")
        except Exception as e:
            update.message.reply_text(f"فشل إرسال الرسالة: {e}")

    def join_room(self, update: Update, context: CallbackContext):
        """Handle join_room command"""
        if len(context.args) < 1:
            update.message.reply_text("استخدم: /join_room [room_id]")
            return
            
        room_id = context.args[0]
        
        # Connect to server if not already connected
        if not self.packet_handler.socket_client:
            self.packet_handler.connect_to_server("98.98.162.80", 39698)
            
        packet = self.packet_handler.join_room(room_id)
        try:
            self.packet_handler.socket_client.send(packet)
            update.message.reply_text(f"تم طلب الانضمام إلى الروم {room_id}")
        except Exception as e:
            update.message.reply_text(f"فشل طلب الانضمام: {e}")

    def run(self):
        """Start the bot"""
        self.updater.start_polling()
        self.updater.idle()


if __name__ == "__main__":
    # Initialize packet handler
    packet_handler = GamePacketHandler()
    
    # Initialize and run Telegram bot (replace with your actual token)
    bot_token = "8090182769:AAGNbboWgdgr4_16fzw4PM4rfCmd6gYOsFE"
    telegram_bot = TelegramBotHandler(bot_token, packet_handler)
    telegram_bot.run()