package com.company;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Scanner;
import java.nio.*;


public class Main {
	private static ArrayList<File> all;
	public static void main(String[] args) {
		File dp = new File("/home/mehrdad/new");

		all=new ArrayList<>();
		listFilesForFolder(dp);

		for(File fl:all)
			System.out.println(fl.getName());

		System.out.println(all.size());
		for(File fl:all) {
			try {
				Scanner myReader = new Scanner(fl);
				String str="/home/mehrdad/new/" + fl.getName();
				File mf=new File(str);
				mf.createNewFile();
				FileWriter myWriter = new FileWriter(mf);

				while (myReader.hasNextLine()) {
					String data = myReader.nextLine();
					//System.out.println(data);
					if (data.contains("<template>")) {
						myWriter.write("<template>");
						myWriter.write('\n');
						myWriter.write("<think><set name=\"language\">english</set></think>");
						myWriter.write('\n');


					} else {
						myWriter.write(data);
						myWriter.write('\n');
					}

				}
				myWriter.close();
				myReader.close();

				System.out.println("Successfully wrote to the file.");
			} catch (IOException e) {
				System.out.println("An error occurred.");
				e.printStackTrace();
			}
		}

	}


	public static void listFilesForFolder(final File folder) {
		for (final File fileEntry : folder.listFiles()) {
			if (fileEntry.isDirectory()) {
				listFilesForFolder(fileEntry);
			} else {
				//System.out.println(folder.isDirectory());
				all.add(fileEntry);
			}
		}
	}
}

