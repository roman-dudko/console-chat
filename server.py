from resourses.Server import Server


if __name__ == '__main__':
    server = Server("127.0.1.1", 7777)
    server.run()
