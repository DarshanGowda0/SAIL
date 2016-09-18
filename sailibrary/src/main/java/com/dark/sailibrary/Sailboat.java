package com.dark.sailibrary;

import android.annotation.TargetApi;
import android.app.Activity;
import android.content.Intent;
import android.os.Build;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.speech.RecognitionListener;
import android.speech.RecognizerIntent;
import android.speech.SpeechRecognizer;
import android.support.annotation.NonNull;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.google.android.gms.tasks.OnFailureListener;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.UnsupportedEncodingException;
import java.net.URLEncoder;
import java.util.ArrayList;
import java.util.HashMap;

/**
 * Created by Rohan on 9/17/2016.
 */
public class Sailboat implements RecognitionListener {

    FirebaseDatabase database;
    DatabaseReference databaseReference;
    Activity activity;
    ArrayList<Integer> listOfIds;
    String TAG = "Test";
    private SpeechRecognizer speech = null;
    private Intent recognizerIntent;

    //chathead variables


    public Sailboat() {
        database = FirebaseDatabase.getInstance();
        databaseReference = database.getReference();

    }


    public void initialize(Activity activity, ArrayList<Integer> listOfIds) {
        this.activity = activity;
        this.listOfIds = listOfIds;


        // first time add the hint to thr firebase db
        if (!PreferenceManager.getDefaultSharedPreferences(activity).getBoolean("init", false)) {
            PreferenceManager.getDefaultSharedPreferences(activity).edit().putBoolean("init", true).apply();
            sendInfo();
        }
        startListener();
        showChatHead();

    }

    private void showChatHead() {
        activity.startService(new Intent(activity, ChatHeadService.class));
    }

    private void startListener() {
        speech = SpeechRecognizer.createSpeechRecognizer(activity);
        speech.setRecognitionListener(this);


        recognizerIntent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
        recognizerIntent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_PREFERENCE,
                "en");
        recognizerIntent.putExtra(RecognizerIntent.EXTRA_CALLING_PACKAGE,
                activity.getPackageName());
        recognizerIntent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL,
                RecognizerIntent.LANGUAGE_MODEL_WEB_SEARCH);
        recognizerIntent.putExtra(RecognizerIntent.EXTRA_MAX_RESULTS, 3);


        speech.startListening(recognizerIntent);

    }


    @TargetApi(Build.VERSION_CODES.M)
    private void sendInfo() {

        String packageName = activity.getPackageName().replaceAll("\\.", "_");
        String activityName = activity.getClass().getSimpleName();

        Log.d(TAG, "sendInfo: " + activityName);

        HashMap<String, HashMap<String, String>> views = new HashMap<>();

        for (int i = 0; i < listOfIds.size(); i++) {
            View v = (activity.findViewById(listOfIds.get(i)));
            String text;
            try {
                text = ((TextView) v).getHint().toString();
            } catch (Exception e) {
                text = ((TextView) v).getText().toString();
//                v.getClass().getName()
//                String test = (String) (v).getAccessibilityClassName();
//                Log.d(TAG, "sendInfo: " + test);
                e.printStackTrace();
            }

            Log.d(TAG, "sendInfo: id " + listOfIds.get(i));
            Log.d(TAG, "sendInfo: text " + text);
            String key = databaseReference.child("packages/" + packageName + "/bucket/"+listOfIds.get(i)).push().getKey();

//            HashMap<String, String> hash = new HashMap<>();
//            hash.put(key, text);
//            views.put("" + listOfIds.get(i), hash);

            databaseReference.child("packages/" + packageName + "/bucket/"+listOfIds.get(i)+"/"+key).setValue(text)
                    .addOnSuccessListener(new OnSuccessListener<Void>() {
                        @Override
                        public void onSuccess(Void aVoid) {
                            Log.d("TAG", "onSuccess: ");

                        }
                    }).addOnFailureListener(new OnFailureListener() {
                @Override
                public void onFailure(@NonNull Exception e) {
                    Log.d("TAG", "onFailure: " + e);
                }
            });
        }

        /*
//        HashMap<String, Object> activityHash = new HashMap<>();
//        activityHash.put("views", views);
//
//        HashMap<String, Object> packageHash = new HashMap<>();
//        packageHash.put(activityName, activityHash);

//        HashMap<String,Object> rootHash = new HashMap<>();
//        rootHash.put("activities",packageHash);
//        packageHash.put("temp","HEllo");
            */



    }


    @Override
    public void onReadyForSpeech(Bundle bundle) {

    }

    @Override
    public void onBeginningOfSpeech() {
        Log.d(TAG, "onBeginningOfSpeech: ");

    }

    @Override
    public void onRmsChanged(float v) {

    }

    @Override
    public void onBufferReceived(byte[] bytes) {

    }

    @Override
    public void onEndOfSpeech() {
        Log.d(TAG, "onEndOfSpeech: ");

    }

    @Override
    public void onError(int i) {
//        speech.stopListening();
        String errorMessage = getErrorText(i);
        Log.d(TAG, "FAILED " + errorMessage);

        startListener();

//        speech.startListening(recognizerIntent);


    }

    @Override
    public void onResults(Bundle bundle) {
        ArrayList<String> matches = bundle
                .getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION);
        String text = "";
        for (String result : matches) {
            text += result + "\n";
            if (result.toLowerCase().startsWith("candy")) {
                Log.d(TAG, "onResults: send this to chandy:" + result.substring(5));
                ChatHeadService.chatHead.setImageResource(R.drawable.microphone_listening);
                sendData(result.substring(5));
                break;
            }
            if (result.toLowerCase().contains("goodbye candy")) {
                ChatHeadService.chatHead.setImageResource(R.drawable.microphone_standby);
                Log.d(TAG, "onResults: bye candy");
                speech.stopListening();
                speech.destroy();
            }
        }
        Log.i(TAG, "onResults:" + text);

        startListener();


    }

    private void sendData(final String speech) {
        // Instantiate the RequestQueue.
        RequestQueue queue = Volley.newRequestQueue(activity);
        try {
            String query = URLEncoder.encode("\"package\":\"" + activity.getPackageName().replaceAll("\\.", "_") + "\",\"view\":\"univ\",\"message\":\"" + speech + "\"", "utf-8");
            String url = "http://204.152.203.111:8000/predictThisLevel/?format=json&json={" + query + "}";
// Request a string response from the provided URL.
            StringRequest stringRequest = new StringRequest(Request.Method.GET, url,
                    new Response.Listener<String>() {
                        @Override
                        public void onResponse(String response) {
                            // Display the first 500 characters of the response string.
//                        mTextView.setText("Response is: "+ response.substring(0,500));
                            Log.d(TAG, "onResponse: " + response);
                            parseResponse(response,speech);
                            ChatHeadService.chatHead.setImageResource(R.drawable.microphone_standby );
                        }
                    }, new Response.ErrorListener() {
                @Override
                public void onErrorResponse(VolleyError error) {
                }
            });

// Add the request to the RequestQueue.
            queue.add(stringRequest);

        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        }

    }

    private void parseResponse(String response, String speech) {
        Integer id = 0;
        String splitString = "";

        try {
            JSONObject json = new JSONObject(response);
            Double confidence = Double.parseDouble(json.getString("accurecy"));
            id = Integer.parseInt(json.getString("shortcode"));
            splitString = json.getString("split_string");

        } catch (JSONException e) {
            e.printStackTrace();
        }

        if (listOfIds.contains(id)) {
            View view = activity.findViewById(id);
            Log.d(TAG, "parseResponse: " + view.getClass().getName());
            if (view.hasOnClickListeners()) {
                view.callOnClick();
            } else {
                ((EditText) view).setText(splitString);
            }

            trainTheApp(speech,id+"");

        }
    }

    private void trainTheApp(String speech,String id) {
        String key = databaseReference.child("packages/" + activity.getPackageName().replaceAll("\\.","_") + "/bucket/"+id).push().getKey();
        databaseReference.child("packages/" + activity.getPackageName().replaceAll("\\.","_") + "/bucket/"+id+"/"+key).setValue(speech)
                .addOnSuccessListener(new OnSuccessListener<Void>() {
                    @Override
                    public void onSuccess(Void aVoid) {
                        Log.d("TAG", "onSuccess: ");

                    }
                }).addOnFailureListener(new OnFailureListener() {
            @Override
            public void onFailure(@NonNull Exception e) {
                Log.d("TAG", "onFailure: " + e);
            }
        });
    }

    @Override
    public void onPartialResults(Bundle bundle) {

    }

    @Override
    public void onEvent(int i, Bundle bundle) {

    }

    public static String getErrorText(int errorCode) {
        String message;
        switch (errorCode) {
            case SpeechRecognizer.ERROR_AUDIO:
                message = "Audio recording error";
                break;
            case SpeechRecognizer.ERROR_CLIENT:
                message = "Client side error";
                break;
            case SpeechRecognizer.ERROR_INSUFFICIENT_PERMISSIONS:
                message = "Insufficient permissions";
                break;
            case SpeechRecognizer.ERROR_NETWORK:
                message = "Network error";
                break;
            case SpeechRecognizer.ERROR_NETWORK_TIMEOUT:
                message = "Network timeout";
                break;
            case SpeechRecognizer.ERROR_NO_MATCH:
                message = "No match";
                break;
            case SpeechRecognizer.ERROR_RECOGNIZER_BUSY:
                message = "RecognitionService busy";
                break;
            case SpeechRecognizer.ERROR_SERVER:
                message = "error from server";
                break;
            case SpeechRecognizer.ERROR_SPEECH_TIMEOUT:
                message = "No speech input";
                break;
            default:
                message = "Didn't understand, please try again.";
                break;
        }
        return message;
    }


    public void destroy() {
        speech.destroy();
        activity.stopService(new Intent(activity, ChatHeadService.class));

    }


}
