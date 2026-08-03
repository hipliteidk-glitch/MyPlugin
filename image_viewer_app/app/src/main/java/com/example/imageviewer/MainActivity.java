package com.example.imageviewer;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {
    private ImageView imageView;
    private int currentImage = 0;
    
    // ================================================================
    // EDIT YOUR IMAGES HERE - Change these to your own images!
    // Put your image files in: app/src/main/res/drawable/
    // Then reference them as R.drawable.your_image_name
    // ================================================================
    private int[] imageResources = {
        R.drawable.image1,
        R.drawable.image2,
        R.drawable.image3,
        R.drawable.image4,
        R.drawable.image5
    };
    // ================================================================

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        imageView = findViewById(R.id.imageView);
        Button changeButton = findViewById(R.id.changeButton);
        Button prevButton = findViewById(R.id.prevButton);

        // Set initial image
        if (imageResources.length > 0) {
            imageView.setImageResource(imageResources[0]);
        }

        // Next image
        changeButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (imageResources.length > 0) {
                    currentImage = (currentImage + 1) % imageResources.length;
                    imageView.setImageResource(imageResources[currentImage]);
                }
            }
        });

        // Previous image
        prevButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (imageResources.length > 0) {
                    currentImage = (currentImage - 1 + imageResources.length) % imageResources.length;
                    imageView.setImageResource(imageResources[currentImage]);
                }
            }
        });

        // Long press to reset to first image
        imageView.setOnLongClickListener(new View.OnLongClickListener() {
            @Override
            public boolean onLongClick(View v) {
                currentImage = 0;
                if (imageResources.length > 0) {
                    imageView.setImageResource(imageResources[0]);
                }
                return true;
            }
        });
    }
}
