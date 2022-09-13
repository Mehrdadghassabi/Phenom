package com.company;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Scanner;


public class Main {

	public static void main(String[] args) {
		try {
			File myObj = new File("tex.txt");
			Scanner myReader = new Scanner(myObj);
			FileWriter myWriter = new FileWriter("filename.txt");
			while (myReader.hasNextLine()) {
				String data = myReader.nextLine();
                  System.out.println(data);
				if(data.contains("<template>")){
					myWriter.write("<template>");
					myWriter.write('\n');
					myWriter.write("<think><set name=\"language\">persian</set></think>");
					myWriter.write('\n');


				}
				else{
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

