from Echecs import *
import cProfile

def main():
    partie = Echecs()
    partie.debut_partie()

if __name__ == "__main__":
    cProfile.run("main()", sort="cumulative")
