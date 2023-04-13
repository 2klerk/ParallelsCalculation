import pycuda.driver as cuda
import pycuda.autoinit
import numpy as np
from pycuda.compiler import SourceModule

mod = SourceModule("""
inline void GPUassert(cudaError_t code, char * file, int line, bool Abort=true)
{
    if (code != 0) {
        fprintf(stderr, "GPUassert: %s %s %d\n", cudaGetErrorString(code),file,line);
        if (Abort) exit(code);
    }       
}

#define GPUerrchk(ans) { GPUassert((ans), FILE, LINE); }

__device__ void swap(char *x, char *y)
{
    char temp;
    temp = *x;
    *x = *y;
    *y = temp;
}

__device__ void permute_device(char *a, int i, int n, int tid, int* count) 
{
    if (i == n) { 
        char b[4]; char* c = a - 1; 
        b[0] = c[0]; b[1] = c[1]; b[2] = c[2]; b[3] = c[3];
        printf("Permutation nr. %i from thread nr. %i is equal to %s\n", count[0], tid, c); count[0] = count[0] + 1; 
    }
    else
    {
        for (int j = i; j <= n; j++)
        {
            swap((a+i), (a+j));
            permute_device(a, i+1, n, tid, count);
            swap((a+i), (a+j)); //backtrack
        }
    }
} 

__global__ void permute_kernel(char* d_A, int size) {

    int tid = threadIdx.x + blockIdx.x * blockDim.x;
    int count[1]; count[0] = 0;

    char local_array[4];

    for (int i=0; i<size; i++) local_array[i] = d_A[i];

    swap(local_array+threadIdx.x,local_array);
    permute_device(local_array+1,0,2,tid,count);

}
""")

h_a = np.array([b'A', b'B', b'C', b'D'])

d_a = cuda.mem_alloc(h_a.nbytes)
cuda.memcpy_htod(d_a, h_a)

print("\n\nPermutations on GPU\n")
permute_kernel = mod.get_function("permute_kernel")

permute_kernel(d_a, np.int32(4), block=(4, 1, 1), grid=(1, 1, 1))

cuda.Context.synchronize()
print("Finished")