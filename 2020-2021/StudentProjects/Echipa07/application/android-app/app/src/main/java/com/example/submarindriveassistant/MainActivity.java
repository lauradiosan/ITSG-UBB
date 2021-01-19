package com.example.submarindriveassistant;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;

import android.Manifest;
import android.app.Activity;
import android.content.ActivityNotFoundException;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.location.Location;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.provider.MediaStore;
import android.util.Base64;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.example.submarindriveassistant.utils.LocationUtil;
import com.example.submarindriveassistant.utils.SocketUtil;
import com.example.submarindriveassistant.utils.SpeedUtil;
import com.example.submarindriveassistant.utils.WeatherUtil;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.net.URI;
import java.io.ByteArrayOutputStream;
import java.nio.charset.StandardCharsets;


public class MainActivity extends AppCompatActivity {
    static Location currentLocation = null;
    static Context context = null;
    static LocationUtil locationUtil = new LocationUtil();

    private static SocketUtil socketUtil = new SocketUtil();
    static TextView textView2 = null;
    private Intent takePictureIntent;
    private Intent choosePictureFromGalleryIntent;
    private static ImageView photoImageView;
    MainActivity mainActivity;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        context = this;
        checkPermission();
        WeatherUtil.createRequestQueue();
        TextView weatherInfoTextView = (TextView) findViewById(R.id.locationInfo);
        TextView speedTextView = (TextView) findViewById(R.id.speed);
        new SpeedUtil().startShowingSpeed(context, speedTextView, locationUtil);
        Button clickButton = (Button) findViewById(R.id.weatherInfoButton);
        photoImageView = (ImageView) findViewById(R.id.photoImageView);
        takePictureIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        clickButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                currentLocation = locationUtil.getLocation();
                if (currentLocation != null) {
                    WeatherUtil weatherUtil = new WeatherUtil();
                    weatherUtil.setWeatherData(context, currentLocation, weatherInfoTextView);
                } else {
                    weatherInfoTextView.setText("Cannot get location data, please try again later.");
                }
            }
        });
        Button cameraButton = (Button) findViewById(R.id.cameraButton);
        cameraButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                takePhoto(takePictureIntent);
            }
        });

        choosePictureFromGalleryIntent = new Intent(Intent.ACTION_PICK, MediaStore.Images.Media.INTERNAL_CONTENT_URI);;
        Button gallery = (Button) findViewById(R.id.galleryButton);
        gallery.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                chooseFromGallery(choosePictureFromGalleryIntent);
            }
        });
        mainActivity =this;
    }

    public void checkPermission() {
        if (Build.VERSION.SDK_INT >= 23) {
            if (checkSelfPermission(Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED &&
                    checkSelfPermission(android.Manifest.permission.ACCESS_COARSE_LOCATION) == PackageManager.PERMISSION_GRANTED &&
                    checkSelfPermission(Manifest.permission.INTERNET) == PackageManager.PERMISSION_GRANTED
                    && checkSelfPermission(Manifest.permission.CAMERA) == PackageManager.PERMISSION_GRANTED
            ) {
                locationUtil.updateLocationData(context);
                currentLocation = locationUtil.getLocation();
            } else {
                ActivityCompat.requestPermissions(this, new String[]{
                        Manifest.permission.ACCESS_FINE_LOCATION,
                        Manifest.permission.ACCESS_COARSE_LOCATION,
                        Manifest.permission.INTERNET,
                        Manifest.permission.CAMERA}, 1);
            }
        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        if (requestCode == 1 && grantResults[0] == PackageManager.PERMISSION_GRANTED && grantResults[1] == PackageManager.PERMISSION_GRANTED && grantResults[2] == PackageManager.PERMISSION_GRANTED) {
            locationUtil.updateLocationData(context);
            currentLocation = locationUtil.getLocation();
        } else {
            checkPermission();
        }
    }

    public final static int CAPTURE_IMAGE_ACTIVITY_REQUEST_CODE = 1034;

    public void takePhoto(Intent takePictureIntent) {
        if (takePictureIntent != null)
            try {
                ((Activity) MainActivity.getContext()).startActivityForResult(takePictureIntent, CAPTURE_IMAGE_ACTIVITY_REQUEST_CODE);
            } catch (ActivityNotFoundException e) {
                Toast.makeText(this, "Cannot get camera intent!", Toast.LENGTH_SHORT).show();
            }
    }
    private static final int PICK_IMAGE = 100;
    public void chooseFromGallery(Intent takePictureIntent){
        if (takePictureIntent != null)
            try {
                ((Activity) MainActivity.getContext()).startActivityForResult(takePictureIntent, PICK_IMAGE);
            } catch (ActivityNotFoundException e) {
                Toast.makeText(this, "Cannot get gallery intent!", Toast.LENGTH_SHORT).show();
            }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        //Log.i("hello", "hello");
        if (requestCode == CAPTURE_IMAGE_ACTIVITY_REQUEST_CODE) {
            if (resultCode == RESULT_OK) {
                Bitmap takenImage = (Bitmap) data.getExtras().get("data");
                mainActivity.setPicture(takenImage);
            } else {
                Toast.makeText(this, "Picture wasn't taken!", Toast.LENGTH_SHORT).show();
            }
        }else if(requestCode == PICK_IMAGE){
            if (resultCode == RESULT_OK) {
                Uri imageUri = data.getData();
                try {
                    Bitmap bitmap = MediaStore.Images.Media.getBitmap(this.getContentResolver(), imageUri);
                    mainActivity.setPicture(bitmap);
                } catch (IOException e) {
                    e.printStackTrace();
                }

            } else {
                Toast.makeText(this, "No picture selected from the gallery!", Toast.LENGTH_SHORT).show();
            }
        }
    }

    public static Context getContext() {
        return context;
    }

    public static LocationUtil getLocationUtil() {
        return locationUtil;
    }

    public static void setPictureForAIResponse(Bitmap picture){

    }

    public void setPicture(Bitmap picture) {
        JSONObject toSendJSON = new JSONObject();
        try {
            ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
            picture.compress(Bitmap.CompressFormat.JPEG, 100, byteArrayOutputStream);
            byte[] byteArray = byteArrayOutputStream.toByteArray();
            toSendJSON.put("picture", byteArray);
            socketUtil.sendViaSocket(toSendJSON);
        } catch (JSONException e) {
            e.printStackTrace();
        }
        new Thread(new Runnable() {
            public void run() {
                JSONObject response = socketUtil.getResponse();
                if (response != null) {
                    Log.i("from server", response.toString());
                } else {
                    //textView2.setText("Incorrect response from the server.");
                }
                byte[] decodedString = new byte[0];
                try {
                    decodedString = Base64.decode(response.getString("text").getBytes(StandardCharsets.UTF_8), Base64.DEFAULT);
                } catch (JSONException e) {
                    e.printStackTrace();
                }
                Bitmap decodedByte = BitmapFactory.decodeByteArray(decodedString, 0, decodedString.length);
                runOnUiThread(new Runnable() {

                    @Override
                    public void run() {
                        photoImageView.setImageBitmap(decodedByte);
                    }
                });
            }
        }).start();;
    }

}

