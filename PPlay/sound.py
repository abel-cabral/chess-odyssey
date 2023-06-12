class Sound():
    """ATENÇÃO! O arquivo passado deve ser .OGG!!! Se não pode gerar problemas."""
    def __init__(self, music_file, pygame):
        self.pygame = pygame
        self.volume = 50
        self.loop = False
        
        # To reduce audio delay
        self.pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        self.music_file = music_file
        self.set_volume(self.volume)

    def load(self):
        try:
            # self.pygame.mixer.Sound(self.music_file)
            self.pygame.mixer.music.load(self.music_file)
        except self.pygame.error:
            print("Erro ao carregar arquivo: ", self.music_file)

    """Value deve ser um valor entre 0 e 100"""
    def set_volume(self, value):
        if(value >= 100):
            value = 100
        if(value <= 0):
            value = 0

        self.volume = value
        self.pygame.mixer.music.set_volume(value/100)

    def increase_volume(self, value):
        self.set_volume(self.volume + value)

    def decrease_volume(self, value):
        self.set_volume(self.volume - value)

    def is_playing(self):
        if(self.pygame.mixer.get_busy()):
            return True
        else:
            return False

    def pause(self):
        self.pygame.mixer.pause()

    def unpause(self):
        self.pygame.mixer.unpause()

    def play_trilha_sonora(self):
        self.load()
        self.pygame.mixer.music.play()
    
    def play_som(self):
        sound = self.pygame.mixer.Sound(self.music_file)
        sound.play()
    
    def stop(self):
        self.pygame.mixer.music.stop()

    def set_repeat(self, repeat):
        self.loop = repeat

    def fadeout(self, time_ms):
       self.pygame.mixer.music.fadeout(time_ms)


