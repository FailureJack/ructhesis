int main(void)
{
    int M = 4096;
    int N = 4096;
    int TASKLET_NUM = 16;
    int Vector[M];
    int Matrix[M][N];
    int LUT[256][256];
    uint FP8_TO_INT32[256];
    int tasklet_id = me();
    int width = N / TASKLET_NUM;

    int Result[N];

    for (int i = 0; i < 16; i++)
    {
        int SubLUT[16][256] = mram_read(LUT[i * 16...i * 16 + 15][256]);
        for (int j = 0; j < M; j++)
        {
            if (Vector[j] < i * 16 || Vector[j] > i * 16 + 15)
            {
                continue;
            }

            int MatRow[N] = mram_read(Matrix[j]);

            for (int k = tasklet_id * width; k < tasklet_id * width + width; k++)
            {
                Result[k] += SubLUT[Vector[j] & 0xF][MatRow[k]];
            }
        }
    }

    BinarySearch(Result[tasklet_id * width... tasklet_id * width + width], FP8_TO_INT32);
    return 0;
}

int main(void)
{
    int M = 4096;
    int N = 4096;
    int TASKLET_NUM = 16;
    int Vector[M];
    int Matrix[M][N];
    int LUT[256][256];
    int FP8_TO_INT32[256];
    int SubMat[128][128];
    int Index[128];
    int Offset[128];
    int tasklet_id = me();
    int width = N / TASKLET_NUM;

    int Result[N];

    for (int i = 0; i < 16; i++)
    {
        int SubLUT[16][256] = mram_read(LUT[i * 16...i * 16 + 15][256]);

        int vidx = 0;
        while (vidx < M)
        {
            int row = 0;
            for (; row < BR && vidx < M; row++, vidx++)
            {
                if (Vector[vidx] < i * 16 || Vector[vidx] > i * 16 + 15)
                {
                    continue;
                }
                Index[row] = vidx;
                Offset[row] = SubLUT[Vector[vidx] & 0xF];
            }
            for (int j = 0; j < N; j += BC)
            {
                for (int k = 0; k < row; k++)
                {
                    mram_read(SubMat[k], Matrix[Index[k]][j]);
                }
                for (int k = j; k < j + BC; k++)
                {
                    int temp = Result_32[k];
                    for (int l = 0; l < row; l++)
                    {
                        temp += *(Offset[l] + SubMat[l][k] * ele_width);
                    }
                    Result_32[k] = temp;
                }
            }
        }
    }

    BinarySearch(Result[tasklet_id * width... tasklet_id * width + width], FP8_TO_INT32);
    return 0;
}