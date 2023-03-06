import { Component, OnInit } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {environment} from "../../../environments/environment";

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.less']
})
export class DashboardComponent implements OnInit {

  classifyUrl = environment.apiUrl + "/classification/predict";

  fileToUpload: any;
  imageUrl: any;
  fileUploaded = false;
  answerLabel = "Upload an image to be classified..."

  constructor(private httpClient: HttpClient) { }

  ngOnInit(): void {

  }

  handleFileInput(target: any) {

    this.fileToUpload = target.files.item(0);

    //Show image preview
    let reader = new FileReader();
    reader.onload = (event: any) => {
      this.imageUrl = event.target.result;
    }
    reader.readAsDataURL(this.fileToUpload);
    this.fileUploaded = true;

    this.answerLabel = "Click 'Classify' button to get results!"
  }

  predictDigit(){
    const formData = new FormData();
    formData.append('image', this.fileToUpload);

    this.httpClient.post<number>(this.classifyUrl, formData).subscribe((data)=>{
      console.log(data);
      if(data >= 0){
        this.answerLabel = "Your digit is: " + data;
      }
      else{
        this.answerLabel = "Invalid input data!"
      }
    });
  }

}
