class Sound:
    BGM = 'music/pleasant_stroll.mp3'
    WALK_SOUND = 'music/walk_on_ground.mp3'
    JUMP_SOUND = 'music/jump.mp3'
    # LANDING_OF_JUMP_SOUND = 'music/landing_of_jump.mp3'
    # SET_BLOCK_SOUND = 'music/open_the_door1.mp3'
    # BREAK_BLOCK_SOUND = 'music/heavy_punch2.mp3'

    def __init__(self):
        # Allow playing two music files at the same time.
        self.musicManager.setConcurrentSoundLimit(3)

        # bgm
        self.bgm = self.loader.loadMusic(Sound.BGM)
        self.bgm.setLoop(True)
        # self.bgm.setVolume(0.5)  # ボリューム
        # self.bgm.setPlayRate(0.75)  # テンポ
        self.bgm.play()

        # sound effect
        self.walk_sound = self.loader.loadMusic(Sound.WALK_SOUND)
        self.walk_sound.setLoop(True)
        self.jump_sound = self.loader.loadMusic(Sound.JUMP_SOUND)
        # self.landing_of_jump_sound = self.loader.loadMusic(Sound.LANDING_OF_JUMP_SOUND)
        # self.set_block_sound = self.loader.loadMusic(Sound.SET_BLOCK_SOUND)
        # self.break_sound = self.loader.loadMusic(Sound.BREAK_BLOCK_SOUND)
