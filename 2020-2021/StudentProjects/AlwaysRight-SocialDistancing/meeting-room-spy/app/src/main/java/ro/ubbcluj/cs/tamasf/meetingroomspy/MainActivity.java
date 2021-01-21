package ro.ubbcluj.cs.tamasf.meetingroomspy;

import android.Manifest;
import android.app.Activity;
import android.content.pm.PackageManager;
import android.media.Image;
import android.media.ImageReader;
import android.os.Bundle;
import android.os.Handler;
import android.os.HandlerThread;
import android.util.Log;

import java.nio.ByteBuffer;

public class MainActivity extends Activity {
    private Camera mCamera;
    private HandlerThread mCameraThread;
    private Handler mCameraHandler;
    private ImageManager mImageManager;
    private Thread imageCaptureThread;
    private static final String TAG = Camera.class.getSimpleName();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        if (checkSelfPermission(Manifest.permission.CAMERA)
                != PackageManager.PERMISSION_GRANTED) {
            Log.e(TAG, "No permission");
            return;
        }

        // prepare the camera
        mCameraThread = new HandlerThread("CameraBackground");
        mCameraThread.start();
        mCameraHandler = new Handler(mCameraThread.getLooper());
        mCamera = Camera.getInstance();
        mCamera.initializeCamera(this, mCameraHandler, mOnImageAvailableListener);
        // image manager prep
        mImageManager = ImageManager.getInstance();

        imageCaptureThread = new Thread(new Runnable() {
            @Override
            public void run() {
                captureImageLoop();
            }
        });

        imageCaptureThread.start();
        CamService.startServer(this);
    }

    private void captureImageLoop() {
        do {
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    mCamera.takePicture();
                }
            });

            // we will take a picture every 5 seconds
            try {
                Thread.sleep(5000);
            } catch (InterruptedException e) {
                Log.e(TAG, e.getMessage());
                break;
            }
        }while(true);
    }

    private ImageReader.OnImageAvailableListener mOnImageAvailableListener =
            new ImageReader.OnImageAvailableListener() {
                @Override
                public void onImageAvailable(ImageReader reader) {
                    Image image = reader.acquireLatestImage();
                    ByteBuffer imageBuf = image.getPlanes()[0].getBuffer();
                    final byte[] imageBytes = new byte[imageBuf.remaining()];
                    imageBuf.get(imageBytes);
                    image.close();
                    mImageManager.setImage(imageBytes);
                    Log.i(TAG, "Image saved.");
                }
            };

    @Override
    protected void onDestroy() {
        super.onDestroy();
        imageCaptureThread.interrupt();
        mCamera.shutDown();
        mCameraThread.quitSafely();
        CamService.stopServer(this);
    }
}
