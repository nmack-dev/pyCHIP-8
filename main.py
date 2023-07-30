from chip8.emulator import Emulator

def main():
    emulator = Emulator()
    emulator.load_rom("roms/test_opcode.ch8")
    emulator.run()

if __name__ == "__main__":
    main()