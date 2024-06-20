import jax.numpy as onp
class _ArrayAPINameSpace:


    abs = onp.abs
    acos = onp.acos
    acosh = onp.acosh
    add = onp.add
    all = onp.all
    any = onp.any
    arange = onp.arange
    argmax = onp.argmax
    argmin = onp.argmin
    argsort = onp.argsort
    asarray = onp.asarray
    asin = onp.asin
    asinh = onp.asinh
    astype = onp.astype
    atan = onp.atan
    atan2 = onp.atan2
    atanh = onp.atanh
    bitwise_and = onp.bitwise_and
    bitwise_invert = onp.bitwise_invert
    bitwise_left_shift = onp.bitwise_left_shift
    bitwise_or = onp.bitwise_or
    bitwise_right_shift = onp.bitwise_right_shift
    bitwise_xor = onp.bitwise_xor
    bool = onp.bool
    broadcast_arrays = onp.broadcast_arrays
    broadcast_to = onp.broadcast_to
    can_cast = onp.can_cast
    ceil = onp.ceil
    complex128 = onp.complex128
    complex64 = onp.complex64
    concat = onp.concat
    conj = onp.conj
    cos = onp.cos
    cosh = onp.cosh
    divide = onp.divide
    e = onp.e
    empty = onp.empty
    empty_like = onp.empty_like
    equal = onp.equal
    exp = onp.exp
    expand_dims = onp.expand_dims
    expm1 = onp.expm1
    eye = onp.eye
    fft = onp.fft
    finfo = onp.finfo
    flip = onp.flip
    float32 = onp.float32
    float64 = onp.float64
    floor = onp.floor
    floor_divide = onp.floor_divide
    from_dlpack = onp.from_dlpack
    full = onp.full
    full_like = onp.full_like
    greater = onp.greater
    greater_equal = onp.greater_equal
    iinfo = onp.iinfo
    imag = onp.imag
    inf = onp.inf
    int16 = onp.int16
    int32 = onp.int32
    int64 = onp.int64
    int8 = onp.int8
    isdtype = onp.isdtype
    isfinite = onp.isfinite
    isinf = onp.isinf
    isnan = onp.isnan
    less = onp.less
    less_equal = onp.less_equal
    linalg = onp.linalg
    linspace = onp.linspace
    log = onp.log
    log10 = onp.log10
    log1p = onp.log1p
    log2 = onp.log2
    logaddexp = onp.logaddexp
    logical_and = onp.logical_and
    logical_not = onp.logical_not
    logical_or = onp.logical_or
    logical_xor = onp.logical_xor
    matmul = onp.matmul
    matrix_transpose = onp.matrix_transpose
    max = onp.max
    mean = onp.mean
    meshgrid = onp.meshgrid
    min = onp.min
    multiply = onp.multiply
    nan = onp.nan
    negative = onp.negative
    newaxis = onp.newaxis
    nonzero = onp.nonzero
    not_equal = onp.not_equal
    ones = onp.ones
    ones_like = onp.ones_like
    permute_dims = onp.permute_dims
    pi = onp.pi
    positive = onp.positive
    pow = onp.pow
    prod = onp.prod
    real = onp.real
    remainder = onp.remainder
    reshape = onp.reshape
    result_type = onp.result_type
    roll = onp.roll
    round = onp.round
    sign = onp.sign
    sin = onp.sin
    sinh = onp.sinh
    sort = onp.sort
    sqrt = onp.sqrt
    square = onp.square
    squeeze = onp.squeeze
    stack = onp.stack
    std = onp.std
    subtract = onp.subtract
    sum = onp.sum
    take = onp.take
    tan = onp.tan
    tanh = onp.tanh
    tensordot = onp.tensordot
    tril = onp.tril
    triu = onp.triu
    trunc = onp.trunc
    uint16 = onp.uint16
    uint32 = onp.uint32
    uint64 = onp.uint64
    uint8 = onp.uint8
    unique_all = onp.unique_all
    unique_counts = onp.unique_counts
    unique_inverse = onp.unique_inverse
    unique_values = onp.unique_values
    var = onp.var
    vecdot = onp.vecdot
    where = onp.where
    zeros = onp.zeros
    zeros_like = onp.zeros_like

    # todo: why not in array_api?
    cumsum = onp.cumsum
    maximum = onp.maximum
    minimum = onp.minimum
    arccos = onp.arccos
    take_along_axis = onp.take_along_axis
    concatenate = onp.concatenate
    hstack = onp.hstack
    split = onp.split
    double = onp.double
    cross = onp.cross