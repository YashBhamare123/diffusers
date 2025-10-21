#!/usr/bin/env python3

# Debug script to understand the height calculation issue
# Based on the error: shape '[1, 16, 95, 2, 64, 2]' is invalid for input of size 262144

def analyze_height_issue():
    # From the error, we can see:
    # - batch_size = 1
    # - num_channels_latents = 16  
    # - height = 95 (this is the problem - it's odd!)
    # - width = 64 (this is fine - it's even)
    
    # The _pack_latents method tries to reshape:
    # latents.view(batch_size, num_channels_latents, height // 2, 2, width // 2, 2)
    # Which becomes: latents.view(1, 16, 95 // 2, 2, 64 // 2, 2)
    # Which becomes: latents.view(1, 16, 47, 2, 32, 2)  # Note: 95 // 2 = 47 (integer division)
    
    # Expected elements in target shape: 1 * 16 * 47 * 2 * 32 * 2 = 48,128
    # But actual tensor size is 262,144
    
    # Let's reverse engineer what the original height should be:
    actual_size = 262144
    batch_size = 1
    num_channels = 16
    width = 64
    
    # If we assume the tensor is currently: [batch_size, num_channels, actual_height, actual_width]
    # Then: actual_size = batch_size * num_channels * actual_height * actual_width
    # So: actual_height = actual_size / (batch_size * num_channels * actual_width)
    
    actual_width = 128  # Let's try different widths
    actual_height = actual_size // (batch_size * num_channels * actual_width)
    print(f"If width={actual_width}, then height={actual_height}")
    
    actual_width = 64
    actual_height = actual_size // (batch_size * num_channels * actual_width)  
    print(f"If width={actual_width}, then height={actual_height}")
    
    # The issue is in the height calculation logic
    # The height needs to be made even before packing
    
    print("\nThe fix should ensure height and width are both even before packing")

if __name__ == "__main__":
    analyze_height_issue()