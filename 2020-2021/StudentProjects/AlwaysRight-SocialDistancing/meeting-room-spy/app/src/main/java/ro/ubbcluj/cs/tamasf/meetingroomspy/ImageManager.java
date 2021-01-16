package ro.ubbcluj.cs.tamasf.meetingroomspy;

class ImageManager {
    private static ImageManager INSTANCE;
    private byte[] imageBytes;

    public static synchronized ImageManager getInstance() {
        if(INSTANCE == null) {
            INSTANCE = new ImageManager();
        }

        return INSTANCE;
    }

    public synchronized void setImage(byte[] imageBytes) {
        this.imageBytes = imageBytes;
    }

    public synchronized byte[] getImage() {
        return this.imageBytes;
    }
}
