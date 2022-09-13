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

				if(data.charAt(0)=='-'){
					myWriter.write("</random>");
					myWriter.write('\n');
					myWriter.write("</template>");
					myWriter.write('\n');
					myWriter.write("</category>");
					myWriter.write('\n');
					myWriter.write('\n');

					myWriter.write("<category>");
					myWriter.write('\n');
					myWriter.write("<pattern>");
					myWriter.write(data.substring(3));
					myWriter.write("</pattern>");
					myWriter.write('\n');
					myWriter.write("<template>");
					myWriter.write('\n');
					myWriter.write("<random>");
					myWriter.write('\n');

				}
				if(data.charAt(0)==' '){
					myWriter.write("<li>");
					myWriter.write(data.substring(3));
					myWriter.write("</li>");
					myWriter.write('\n');


				}
			}
			myWriter.write("</random>");
			myWriter.write('\n');
			myWriter.write("</template>");
			myWriter.write('\n');
			myWriter.write("</category>");

			myWriter.close();
			myReader.close();
			System.out.println("Successfully wrote to the file.");
		} catch (IOException e) {
			System.out.println("An error occurred.");
			e.printStackTrace();
		}
	}
}

