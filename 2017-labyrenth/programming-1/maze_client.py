from socket import create_connection
from solve import get_path

MAZE_SERVER = ('54.69.145.229', 16000)
RECV_SIZE = 8192

def main():
    conn = create_connection(MAZE_SERVER)
    response = conn.recv(RECV_SIZE)
    while True:
        print response
        if "Now " not in response:
            return

        response_lines = response.splitlines()
        find_delim = [x for x in response_lines if x.startswith('Now')][0]
        maze_lines = response_lines[response_lines.index(find_delim)+2:-1]
        maze_text = '\n'.join(maze_lines)

        # Do your thing here with either maze_text or maze_lines.
        #solution = raw_input("Your solution: ")
        solution = get_path(maze_text)
        print "Your solution:", solution

        if not len(solution):
            return
        conn.send(solution)

        response = conn.recv(RECV_SIZE)


if __name__ == '__main__':
    main()
