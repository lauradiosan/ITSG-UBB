package ro.ubbcluj.cs.tamasf.meetingroomspy;

import android.app.IntentService;
import android.content.Context;
import android.content.Intent;
import android.util.Log;

import org.restlet.Component;
import org.restlet.data.Protocol;
import org.restlet.engine.Engine;
import org.restlet.ext.nio.HttpServerHelper;
import org.restlet.routing.Router;

public class CamService extends IntentService {
    private static final String ACTION_START = "ro.ubbcluj.cs.tamasf.meetingroomspy.action.START";
    private static final String ACTION_STOP = "ro.ubbcluj.cs.tamasf.meetingroomspy.action.STOP";
    private static final String TAG = CamService.class.getSimpleName();
    private static final String SERVICE_NAME = "CamService";
    private static final int PORT = 1332;

    private static final String IMAGE_ROUTE = "/image";

    private Component mComponent;

    public CamService() {
        super(SERVICE_NAME);
        Engine.getInstance().getRegisteredServers().clear();
        Engine.getInstance().getRegisteredServers().add(new HttpServerHelper(null));
        mComponent = new Component();
        mComponent.getServers().add(Protocol.HTTP, PORT);
        Router router = new Router(mComponent.getContext().createChildContext());

        router.attach(IMAGE_ROUTE, ImageResource.class);

        mComponent.getDefaultHost().attach("/rest", router);
    }

    public static void startServer(Context context) {
        Intent intent = new Intent(context, CamService.class);
        intent.setAction(ACTION_START);
        context.startService(intent);
    }

    public static void stopServer(Context context) {
        Intent intent = new Intent(context, CamService.class);
        intent.setAction(ACTION_STOP);
        context.startService(intent);
    }


    @Override
    protected void onHandleIntent(Intent intent) {
        if (intent != null) {
            final String action = intent.getAction();
            if (ACTION_START.equals(action)) {
                handleStart();
            } else if (ACTION_STOP.equals(action)) {
                handleStop();
            }
        }
    }

    private void handleStart() {
        try {
            mComponent.start();
        } catch (Exception e) {
            Log.e(TAG, e.toString());
        }
    }

    private void handleStop() {
        try {
            mComponent.stop();
        } catch (Exception e) {
            Log.e(TAG, e.toString());
        }
    }
}
