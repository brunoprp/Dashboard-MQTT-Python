#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 13:41:23 2021

@author: bruno
"""
from collections import Counter
from itertools import chain
from PIL import Image, ImageChops
import time

def count_symbols(image):
    pixels = image.getdata()
    values = chain.from_iterable(pixels)
    counts = Counter(values).items()
    return sorted(counts, key=lambda x:x[::-1])


def build_tree(counts) :
    nodes = [entry[::-1] for entry in counts] # Reverse each (symbol,count) tuple
    while len(nodes) > 1 :
        leastTwo = tuple(nodes[0:2]) # get the 2 to combine
        theRest = nodes[2:] # all the others
        combFreq = leastTwo[0][0] + leastTwo[1][0]  # the branch points freq
        nodes = theRest + [(combFreq, leastTwo)] # add branch point to the end
        print(nodes[0])
        nodes.sort(key=lambda t: t[0]) # sort it into place
    return nodes[0] # Return the single tree inside the list


def trim_tree(tree) :
    p = tree[1] # Ignore freq count in [0]
    if type(p) is tuple: # Node, trim left then right and recombine
        return (trim_tree(p[0]), trim_tree(p[1]))
    return p # Leaf, just return it



def assign_codes_impl(codes, node, pat):
    if type(node) == tuple:
        assign_codes_impl(codes, node[0], pat + [0]) # Branch point. Do the left branch
        assign_codes_impl(codes, node[1], pat + [1]) # then do the right branch.
    else:
        codes[node] = pat # A leaf. set its code

def assign_codes(tree):
    codes = {}
    assign_codes_impl(codes, tree, [])
    return codes


def to_binary_list(n):
    """Convert integer into a list of bits"""
    return [n] if (n <= 1) else to_binary_list(n >> 1) + [n & 1]

def from_binary_list(bits):
    """Convert list of bits into an integer"""
    result = 0
    for bit in bits:
        result = (result << 1) | bit
    return result

def pad_bits(bits, n):
    """Prefix list of bits with enough zeros to reach n digits"""
    assert(n >= len(bits))
    return ([0] * (n - len(bits)) + bits)



class OutputBitStream(object): 
    def __init__(self, file_name): 
        self.file_name = file_name
        self.file = open(self.file_name, 'wb') 
        self.bytes_written = 0
        self.buffer = []

    def write_bit(self, value):
        self.write_bits([value])

    def write_bits(self, values):
        self.buffer += values
        while len(self.buffer) >= 8:
            self._save_byte()        

    def flush(self):
        if len(self.buffer) > 0: # Add trailing zeros to complete a byte and write it
            self.buffer += [0] * (8 - len(self.buffer))
            self._save_byte()
        assert(len(self.buffer) == 0)

    def _save_byte(self):
        bits = self.buffer[:8]
        self.buffer[:] = self.buffer[8:]

        byte_value = from_binary_list(bits)
        self.file.write(bytes([byte_value]))
        self.bytes_written += 1

    def close(self): 
        self.flush()
        self.file.close()
        
        
        
class InputBitStream(object): 
    def __init__(self, file_name): 
        self.file_name = file_name
        self.file = open(self.file_name, 'rb') 
        self.bytes_read = 0
        self.buffer = []

    def read_bit(self):
        return self.read_bits(1)[0]

    def read_bits(self, count):
        while len(self.buffer) < count:
            self._load_byte()
        result = self.buffer[:count]
        self.buffer[:] = self.buffer[count:]
        return result

    def flush(self):
        assert(not any(self.buffer))
        self.buffer[:] = []

    def _load_byte(self):
        value = ord(self.file.read(1))
        self.buffer += pad_bits(to_binary_list(value), 8)
        self.bytes_read += 1

    def close(self): 
        self.file.close()




def compressed_size(counts, codes):
    header_size = 2 * 16 # height and width as 16 bit values

    tree_size = len(counts) * (1 + 8) # Leafs: 1 bit flag, 8 bit symbol each
    tree_size += len(counts) - 1 # Nodes: 1 bit flag each
    if tree_size % 8 > 0: # Padding to next full byte
        tree_size += 8 - (tree_size % 8)

    # Sum for each symbol of count * code length
    pixels_size = sum([count * len(codes[symbol]) for symbol, count in counts])
    if pixels_size % 8 > 0: # Padding to next full byte
        pixels_size += 8 - (pixels_size % 8)

    return (header_size + tree_size + pixels_size) / 8

def encode_header(image, bitstream):
    height_bits = pad_bits(to_binary_list(image.height), 16)
    bitstream.write_bits(height_bits)    
    width_bits = pad_bits(to_binary_list(image.width), 16)
    bitstream.write_bits(width_bits)

def encode_tree(tree, bitstream):
    if type(tree) == tuple: # Note - write 0 and encode children
        bitstream.write_bit(0)
        encode_tree(tree[0], bitstream)
        encode_tree(tree[1], bitstream)
    else: # Leaf - write 1, followed by 8 bit symbol
        bitstream.write_bit(1)
        symbol_bits = pad_bits(to_binary_list(tree), 8)
        bitstream.write_bits(symbol_bits)

def encode_pixels(image, codes, bitstream):
    for pixel in image.getdata():
        for value in pixel:
            bitstream.write_bits(codes[value])
            
            
def raw_size(width, height):
    header_size = 2 * 16 # height and width as 16 bit values
    pixels_size = 3 * 8 * width * height # 3 channels, 8 bits per channel
    return (header_size + pixels_size) / 8
            

def compress_image(in_file_name, out_file_name):
    print('Compressing "%s" -> "%s"' % (in_file_name, out_file_name))
    image = Image.open(in_file_name)
    print('Image shape: (height=%d, width=%d)' % (image.height, image.width))
    size_raw = raw_size(image.height, image.width)
    print('RAW image size: %d bytes' % size_raw)
    counts = count_symbols(image)
    print('Counts: %s' % counts)
    tree = build_tree(counts)
    print('Tree: %s' % str(tree))
    trimmed_tree = trim_tree(tree)
    print('Trimmed tree: %s' % str(trimmed_tree))
    codes = assign_codes(trimmed_tree)
    print('Codes: %s' % codes)

    size_estimate = compressed_size(counts, codes)
    print('Estimated size: %d bytes' % size_estimate)

    print('Writing...')
    stream = OutputBitStream(out_file_name)
    print('* Header offset: %d' % stream.bytes_written)
    encode_header(image, stream)
    stream.flush() # Ensure next chunk is byte-aligned
    print('* Tree offset: %d' % stream.bytes_written)
    encode_tree(trimmed_tree, stream)
    stream.flush() # Ensure next chunk is byte-aligned
    print('* Pixel offset: %d' % stream.bytes_written)
    encode_pixels(image, codes, stream)
    stream.close()

    size_real = stream.bytes_written
    print('Wrote %d bytes.' % size_real)

    print('Estimate is %scorrect.' % ('' if size_estimate == size_real else 'in'))
    print('Compression ratio: %0.2f' % (float(size_raw) / size_real))
    
    
    
def decode_header(bitstream):
    height = from_binary_list(bitstream.read_bits(16))
    width = from_binary_list(bitstream.read_bits(16))
    return (height, width)

# https://stackoverflow.com/a/759766/3962537
def decode_tree(bitstream):
    flag = bitstream.read_bits(1)[0]
    if flag == 1: # Leaf, read and return symbol
        return from_binary_list(bitstream.read_bits(8))
    left = decode_tree(bitstream)
    right = decode_tree(bitstream)
    return (left, right)

def decode_value(tree, bitstream):
    bit = bitstream.read_bits(1)[0]
    node = tree[bit]
    if type(node) == tuple:
        return decode_value(node, bitstream)
    return node

def decode_pixels(height, width, tree, bitstream):
    pixels = bytearray()
    for i in range(height * width * 3):
        pixels.append(decode_value(tree, bitstream))
    return Image.frombytes('RGB', (width, height), bytes(pixels))

def decompress_image(in_file_name, out_file_name):
    print('Decompressing "%s" -> "%s"' % (in_file_name, out_file_name))

    print('Reading...')
    stream = InputBitStream(in_file_name)
    print('* Header offset: %d' % stream.bytes_read)
    height, width = decode_header(stream)
    stream.flush() # Ensure next chunk is byte-aligned
    print('* Tree offset: %d' % stream.bytes_read)    
    trimmed_tree = decode_tree(stream)
    stream.flush() # Ensure next chunk is byte-aligned
    print('* Pixel offset: %d' % stream.bytes_read)
    image = decode_pixels(height, width, trimmed_tree, stream)
    stream.close()
    print('Read %d bytes.' % stream.bytes_read)

    print('Image size: (height=%d, width=%d)' % (height, width))
    print('Trimmed tree: %s' % str(trimmed_tree))
    image.save(out_file_name)
    
    
    
    
def images_equal(file_name_a, file_name_b):
    image_a = Image.open(file_name_a)
    image_b = Image.open(file_name_b)

    diff = ImageChops.difference(image_a, image_b)

    return diff.getbbox() is None

if __name__ == '__main__':
    start = time.time()

    compress_image('input.jpg', 'imagem.txt')

    print('-' * 40)

    decompress_image('imagem.txt', 'image_out.jpg')

    stop = time.time()
    times = (stop - start) * 1000

    print('-' * 40)

    print('Run time takes %d miliseconds' % times)
    print('Images equal = %s' % images_equal('input.jpg', 'image_out.jpg'))