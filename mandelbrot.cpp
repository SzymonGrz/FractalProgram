
#include "pch.h"
#include "mandelbrot.h"
    
    void mandelbrot_set(int width, int height, int max_iteration, int* output, double xmin, double xmax, double ymin, double ymax)
    {

        double x, y;

        double dx = (xmax - xmin) / width;
        double dy = (ymax - ymin) / height;

        double z_real = 0;
        double z_imag = 0;
        double c_real = 0;
        double c_imag = 0;

        int iterations;

        for (int j = 0; j < height; j++)
        {
            y = ymin + j * dy;
            for (int i = 0; i < width; i++)
            {
                x = xmin + i * dx;
                z_real = 0;
                z_imag = 0;
                c_real = x;
                c_imag = y;
                iterations = 0;
                while (z_real * z_real + z_imag * z_imag < 4 && iterations < max_iteration)
                {
                    double z_real2 = z_real * z_real - z_imag * z_imag + c_real;
                    z_imag = 2 * z_real * z_imag + c_imag;
                    z_real = z_real2;
                    iterations++;
                }
                output[j * width + i] = iterations;
            }
        }
    }

    void julia_set(int width, int height, int max_iteration, float c_real, float c_imag, int* output)
    {
        double xmin = -2.0;
        double xmax = 2.0;
        double ymin = -2.0;
        double ymax = 2.0;

        double x, y;

        double dx = (xmax - xmin) / width;
        double dy = (ymax - ymin) / height;

        double z_real = 0;
        double z_imag = 0;

        int iterations;

        for (int j = 0; j < height; j++)
        {
            y = ymin + j * dy;
            for (int i = 0; i < width; i++)
            {
                x = xmin + i * dx;
                z_real = x;
                z_imag = y;
                iterations = 0;
                while (z_real * z_real + z_imag * z_imag < 4 && iterations < max_iteration)
                {
                    double z_real2 = z_real * z_real - z_imag * z_imag + c_real;
                    z_imag = 2 * z_real * z_imag + c_imag;
                    z_real = z_real2;
                    iterations++;
                }
                if (iterations > 0 && iterations < iterations - 30)
                    iterations += 20;
                output[j * width + i] = iterations;
            }
        }
    }
