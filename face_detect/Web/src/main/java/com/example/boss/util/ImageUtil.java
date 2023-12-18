package com.example.boss.util;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.util.Base64;
import java.util.zip.Deflater;
import java.util.zip.Inflater;

import org.springframework.web.multipart.MultipartFile;

public class ImageUtil {
	public static byte[] compressImage(MultipartFile file) {
		byte[] data;
		try {
			data = file.getBytes();
			Deflater deflater = new Deflater();
			deflater.setLevel(Deflater.BEST_COMPRESSION);
			deflater.setInput(data);
			deflater.finish();
			ByteArrayOutputStream outputStream = new ByteArrayOutputStream(data.length);
			byte[] tmp = new byte[4 * 1024];
			while (!deflater.finished()) {
				int size = deflater.deflate(tmp);
				outputStream.write(tmp, 0, size);
			}
			try {
				outputStream.close();
			} catch (Exception ignored) {
			}
			return outputStream.toByteArray();
		} catch (IOException e) {
			e.printStackTrace();
		}
		return null;

	}

	public static String decompressImage(byte[] data) {
		Inflater inflater = new Inflater();
		inflater.setInput(data);
		ByteArrayOutputStream outputStream = new ByteArrayOutputStream(data.length);
		byte[] tmp = new byte[4 * 1024];
		try {
			while (!inflater.finished()) {
				int count = inflater.inflate(tmp);
				outputStream.write(tmp, 0, count);
			}
			outputStream.close();
		} catch (Exception ignored) {
		}
		return Base64.getEncoder().encodeToString(outputStream.toByteArray());
	}
}
