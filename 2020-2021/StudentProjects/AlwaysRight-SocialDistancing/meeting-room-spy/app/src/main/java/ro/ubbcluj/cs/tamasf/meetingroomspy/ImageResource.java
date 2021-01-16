package ro.ubbcluj.cs.tamasf.meetingroomspy;

import android.util.Log;

import org.json.JSONObject;
import org.restlet.data.MediaType;
import org.restlet.representation.Representation;
import org.restlet.representation.StringRepresentation;
import org.restlet.resource.Get;
import org.restlet.resource.ServerResource;

import java.util.Base64;

public class ImageResource extends ServerResource {
    private static final String TAG = ImageResource.class.getSimpleName();
    private static final String ROOM_NAME = "Room #1";

    @Get("json")
    public Representation getImageResource() {
        JSONObject result = new JSONObject();

        try {
            byte[] imageBytes = ImageManager.getInstance().getImage();
            result.put("room_name", ROOM_NAME);

            if(imageBytes != null) {
                String encoded = Base64.getEncoder().encodeToString(imageBytes);
                result.put("image", encoded);
            }
            else {
                result.put("image", "empty");
            }

        } catch (Exception e) {
            Log.e(TAG, e.getMessage());
        }

        return new StringRepresentation(result.toString(), MediaType.APPLICATION_ALL_JSON);
    }
}
