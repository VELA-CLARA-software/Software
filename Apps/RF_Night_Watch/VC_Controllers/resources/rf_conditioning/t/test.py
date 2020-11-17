import os, random
secure_random = random.SystemRandom()
a= os.getcwd()+'\\splash\\'+secure_random.choice(os.listdir(os.getcwd()+'\splash')) #change dir name to whatever		
print a
if __name__ == "__main__":

    app = QApplication(sys.argv)
    #movie = QMovie(os.getcwd()+'\splash\' + random.choice(os.listdir(os.getcwd()+'\splash')))
    movie = QMovie(a)

    splash = MovieSplashScreen(movie)
	
    splash.show()
    
    start = time.time()
    
    while movie.state() == QMovie.Running and time.time() < start + 10:
        app.processEvents()
    
    window = QWidget()
    window.show()
    splash.finish(window)
    
    sys.exit(app.exec_())