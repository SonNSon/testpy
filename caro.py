import pygame
import sys

#khai báo biến vs hằng số
WIDTH, HEIGHT = 800,800
ROWS,COLS = 20,20
SQUARE_SIZE = WIDTH // COLS  #phép chia làm tròn xuống
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
X_COLOR, O_COLOR = (255, 0, 0), (0, 0, 255)  # Đỏ cho 'X', Xanh cho 'O'

# Khởi tạo bảng Caro
board = [[' ' for _ in range(COLS)] for _ in range(ROWS)]  
# tạo ra 1 list gồm gồm các kí tự trắng (" ") với độ dài COLS và lặp với ROWS lần

# Khởi tạo Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
#tạo cửa sổ đồ họa có kích thước là WIDTH x HEIGHT pixels trở thành một đối tượng đại diện cho cửa sổ đồ họa.
pygame.display.set_caption('Caro Game') 
# hiển thị trên thanh tiêu đề của cửa sổ đồ họa
# Hàm để chơi lại trò chơi
def play_again():
    restart_game()  # Đặt lại trạng thái trò chơi
    screen.fill(WHITE)  # Xóa màn hình
    draw_board()  # Vẽ lại bảng
    pygame.display.flip()  # Hiển thị màn hình mới



def draw_board():
    #duyệt qua từng ô trong bảng trò chơi với row và col
    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(screen, WHITE, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))  
            #vẽ ô vuông trắng
            pygame.draw.rect(screen, BLACK, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)
            #vẽ viền đen cho từng ô vuông
            if board[row][col] == 'X': #vẽ dấu X
                pygame.draw.line(screen, X_COLOR, (col * SQUARE_SIZE + 10, row * SQUARE_SIZE + 10), (col * SQUARE_SIZE + SQUARE_SIZE - 10, row * SQUARE_SIZE + SQUARE_SIZE - 10), 4)
                pygame.draw.line(screen, X_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE - 10, row * SQUARE_SIZE + 10), (col * SQUARE_SIZE + 10, row * SQUARE_SIZE + SQUARE_SIZE - 10), 4)
            elif board[row][col] == 'O': # vẽ hình tròn
                pygame.draw.circle(screen, O_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 10, 4)

def check_winner():
    # Kiểm tra hàng và cột
    for i in range(ROWS):
        for j in range(COLS - 4):   #Như đã khai báo ở trên, chỉ cần 5 ô liền nhau sẽ chiến thắng, nên COLS - 4, vì khi 4 ô cuối không còn quan trọng
            if board[i][j] == board[i][j + 1] == board[i][j + 2] == board[i][j + 3] == board[i][j + 4] and board[i][j] != ' ':
                #kiểm tra hàng ngang xem giống nhau không và khác trống
                return True
            if board[j][i] == board[j + 1][i] == board[j + 2][i] == board[j + 3][i] == board[j + 4][i] and board[j][i] != ' ':
                #kiểm tra hàng dọc xem giống nhau không và khác trống
                return True
              
    # Kiểm tra đường chéo chính
    for i in range(ROWS - 4):
        for j in range(COLS - 4):
            if board[i][j] == board[i + 1][j + 1] == board[i + 2][j + 2] == board[i + 3][j + 3] == board[i + 4][j + 4] and board[i][j] != ' ':
                return True

    # Kiểm tra đường chéo phụ
    for i in range(4, ROWS):
        for j in range(COLS - 4):
            if board[i][j] == board[i - 1][j + 1] == board[i - 2][j + 2] == board[i - 3][j + 3] == board[i - 4][j + 4] and board[i][j] != ' ':
                return True

    return False

def restart_game():
    global board, game_over, turn
    board = [[' ' for _ in range(COLS)] for _ in range(ROWS)]
    game_over = False
    turn = 'X'

def show_winner_popup(winner):
    popup_font = pygame.font.Font(None, 48)     #đặt kiểu chữ và kích thước thông báo
    popup_text = popup_font.render(f'Player {winner} wins!', True, WHITE)   #tạo đối tượng surface thông báo đã được render
    
    popup_rect = popup_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    
    pygame.draw.rect(screen, BLACK, (popup_rect.x - 10, popup_rect.y - 10, popup_rect.width + 20, popup_rect.height + 20))
    screen.blit(popup_text, popup_rect)

    pygame.display.flip()
    pygame.time.delay(2000)  # Hiển thị thông báo trong 2 giây(2000 mili giây)

# Vòng lặp chính
turn = 'X'      #xđ người chơi X hay O
game_over = False   #kiểm tra xem game đã kết thúc chưa

while True:     #vòng lặp vô hạn khi điều kiện là True
    for event in pygame.event.get():    #biến event được sử dụng để lặp qua các sự kiện trong Pygame
        #thuộc tính type của pygame.event.get() là để xác định cho các loại sự kiện cụ thể
        if event.type == pygame.QUIT:      #đóng cửa sổ game
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX, mouseY = event.pos      #trả về 1 tuple chứa tọa độ (x,y) của chuột
            #sau đó chuyển đổi thành hàng và cột tương ứng trên màn hình với phép chia nguyên
            clicked_row = mouseY // SQUARE_SIZE         #kết quả là hàng tương ứng trên bảng
            clicked_col = mouseX // SQUARE_SIZE         #kết quả là cột tương ứng trên bảng

            if board[clicked_row][clicked_col] == ' ':      #nếu ô trống thay đổi giá trị thành X hoặc O tùy theo turn
                board[clicked_row][clicked_col] = turn
                if check_winner():
                    print(f'Player {turn} wins!')
                    show_winner_popup(turn)
                    game_over = True            #game_over trả về true kết thúc game
                if turn == 'X':
                    turn = 'O'
                else:
                    turn = 'X'
                # turn = 'O' if turn == 'X' else 'X' (biểu thức ternary: Nếu turn là X thì thay đổi O, không thì thay đổi thành X)
                
        # Xử lý nút chơi lại từ đầu
        elif event.type == pygame.MOUSEBUTTONDOWN and game_over:        #nếu người dùng nhấp chuột sau khi trò chơi đã kết thúc
            if WIDTH // 2 - 75 <= mouseX <= WIDTH // 2 + 75 and HEIGHT // 2 + 50 <= mouseY <= HEIGHT // 2 + 100:
                play_again()

    #xóa màn hình và vẽ lại bảng
    screen.fill(WHITE)
    draw_board()
    if game_over:
        # Thêm nút chơi lại từ đầu
        pygame.draw.rect(screen, BLACK, (WIDTH // 2 - 75, HEIGHT // 2 + 50, 150, 50))
        restart_font = pygame.font.Font(None, 36)
        restart_text = restart_font.render('Play Again', True, WHITE)
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 75))
        screen.blit(restart_text, restart_rect)
        #hàm vẽ nội dung từ 1 bề mặt lên bề mặt khác (blit)

    pygame.display.flip()
