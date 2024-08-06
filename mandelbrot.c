
void mandelbrot_set(int width, int height, int max_iteration, int* output)
{
    double xmin = -2.0;
    double xmax = 1.0;
    double ymin = -1.5;
    double ymax = 1.5;

    double x, y;

    double dx = (xmax - xmin)/ width;
    double dy = (ymax-ymin) /width;

    double z_real = 0;
    double z_imag = 0;
    double c_real = 0;
    double c_imag = 0;

    int iterations;

    for(int i = 0; i < width; i++)
    {
        x = xmin + i * dx;
        for(int j = 0; j < height; j++)
        {   
            y = ymin + j * dy;
            z_real = 0;
            z_imag = 0;    
            c_real = x;
            c_imag = y;
            iterations = 0;
            while(z_real*z_real+z_imag*z_imag < 4 && iterations < max_iteration)
            {
                double z_real2 = z_real*z_real - z_imag*z_imag + c_real;
                z_imag = 2 * z_real* z_imag + c_imag;
                z_real = z_real2;
                iterations++;
            }
            output[j * width +i ] = iterations;
        }
    }

}