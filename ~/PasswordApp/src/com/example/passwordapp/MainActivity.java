package com.example.passwordapp;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {

    private EditText editTextPassword;
    private Button buttonSubmit;

    private static final String PASSWORD_NORMAL = "normal";
    private static final String PASSWORD_SECRET = "secret";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        editTextPassword = findViewById(R.id.editTextPassword);
        buttonSubmit = findViewById(R.id.buttonSubmit);

        buttonSubmit.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String entered = editTextPassword.getText().toString().trim();

                if (entered.isEmpty()) {
                    Toast.makeText(MainActivity.this, "Please enter a password", Toast.LENGTH_SHORT).show();
                    return;
                }

                if (entered.equals(PASSWORD_NORMAL)) {
                    Intent intent = new Intent(MainActivity.this, NormalActivity.class);
                    startActivity(intent);
                } else if (entered.equals(PASSWORD_SECRET)) {
                    Intent intent = new Intent(MainActivity.this, SecretActivity.class);
                    startActivity(intent);
                } else {
                    Toast.makeText(MainActivity.this, "Incorrect password", Toast.LENGTH_SHORT).show();
                }
            }
        });
    }
}