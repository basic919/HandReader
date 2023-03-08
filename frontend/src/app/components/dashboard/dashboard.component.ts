import { Component, OnInit } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {environment} from "../../../environments/environment";
import {AuthService} from "../../auth.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.less']
})
export class DashboardComponent implements OnInit {

  fileToUpload: any;
  imageUrl: any;
  fileUploaded = false;
  answerLabel = "Upload an image to be classified..."

  predictUrl = environment.apiUrl + "/classification/predict";

  classifying: boolean = false;

  constructor(private httpClient: HttpClient, public authService: AuthService, private router: Router) { }

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

  logOut(){
    this.authService.logout();
    this.router.navigate(['/login']);
  }

  predictDigit(){

    this.classifying = true;

    const formData = new FormData();
    formData.append('image', this.fileToUpload);

    this.httpClient.post<number>(this.predictUrl, formData).subscribe((data)=>{
      console.log(data);
      this.classifying = false;
      if(data < 0){
        this.answerLabel = "Invalid input data!"
      }
      else{
        this.answerLabel = "Your digit is: " + data;
      }
    });
  }

}
