package com.dark.sailibrary;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.speech.RecognitionListener;
import android.speech.RecognizerIntent;
import android.speech.SpeechRecognizer;
import android.support.annotation.NonNull;
import android.util.Log;
import android.view.View;
import android.widget.TextView;

import com.google.android.gms.tasks.OnFailureListener;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;

import java.util.ArrayList;
import java.util.HashMap;

/**
 * Created by Rohan on 9/17/2016.
 */
public class Sailboat implements RecognitionListener {

    FirebaseDatabase database;
    DatabaseReference databaseReference;
    Activity activity;
    ArrayList<ViewObject> listOfIds;
    String TAG = "Test";
    private SpeechRecognizer speech = null;
    private Intent recognizerIntent;



    public Sailboat() {

        database = FirebaseDatabase.getInstance();
        databaseReference = database.getReference();

    }

    public void destroy(){
        speech.destroy();
    }

    public void initialize(Activity activity, ArrayList<ViewObject> listOfIds) {
        this.activity = activity;
        this.listOfIds = listOfIds;

        sendInfo();
        startListener();

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



    private void sendInfo() {

        String packageName = activity.getPackageName().replaceAll("\\.", "_");
        String activityName = activity.getClass().getSimpleName();

        Log.d(TAG, "sendInfo: " + activityName);

        HashMap<String, HashMap<String, String>> views = new HashMap<>();

        for (int i = 0; i < listOfIds.size(); i++) {
            View v = (activity.findViewById(listOfIds.get(i).id));
            String text;
            try {
                text = ((TextView) v).getHint().toString();
            } catch (Exception e) {
                text = ((TextView) v).getText().toString();
                e.printStackTrace();
            }

            Log.d(TAG, "sendInfo: id " + listOfIds.get(i).id);
            Log.d(TAG, "sendInfo: text " + text);
            HashMap<String, String> hash = new HashMap<>();
            hash.put("hint", text);
            views.put("" + listOfIds.get(i).id, hash);
        }

        HashMap<String, Object> activityHash = new HashMap<>();
        activityHash.put("views", views);

        HashMap<String, Object> packageHash = new HashMap<>();
        packageHash.put(activityName, activityHash);

//        HashMap<String,Object> rootHash = new HashMap<>();
//        rootHash.put("activities",packageHash);
//        packageHash.put("temp","HEllo");


        databaseReference.child("packages/" + packageName + "/activities").setValue(packageHash)
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
            if (result.toLowerCase().startsWith("candy")){
                Log.d(TAG, "onResults: send this to chandy:"+result.substring(5));
                break;
            }
            if (result.toLowerCase().contains("bye candy")){
                Log.d(TAG, "onResults: bye candy");
                speech.stopListening();
            }
        }
        Log.i(TAG, "onResults:"+text);

        startListener();


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

}
