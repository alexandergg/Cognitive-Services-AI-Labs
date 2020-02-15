import sys, time, wget, os

from settings.settings import Settings
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "."))

class CustomVision():
    def __init__(self):
        self._settings = Settings()
        self._endpoint = self._settings.get_endpoint()
        self._sample_project_name = self._settings.get_project_name()
        self._publish_iteration_name = "Iteration1"
        self._prediction_resource_id = self._settings.get_prediction_resource_id()
        self._subscription_training_key = self._settings.get_subscription_training_key()
        self._subscription_prediction_key = self._settings.get_subscription_prediction_key()
        self._images_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self._trainer = CustomVisionTrainingClient(self._subscription_training_key, endpoint=self._endpoint)
        self._predictor = CustomVisionPredictionClient(self._subscription_prediction_key, endpoint=self._endpoint)

    def find_project(self):
        for proj in self._trainer.get_projects():
            if proj.name == self._sample_project_name:
                return proj

    def create_project(self):
        print("Creating project...")
        return self._trainer.create_project(self._sample_project_name)   

    def uploadData(self, project):
        newspapers_tag = self._trainer.create_tag(project.id, "Newspapers")
        oldnewspapers_tag = self._trainer.create_tag(project.id, "Oldnewspapers")

        print("Adding images...")
        newspapers_dir = os.path.join(self._images_folder, "Newspapers")
        for image in os.listdir(newspapers_dir):
            with open(os.path.join(newspapers_dir, image), mode="rb") as img_data:
                self._trainer.create_images_from_data(
                    project.id, img_data.read(), [newspapers_tag.id])

        old_newspapers_dir = os.path.join(self._images_folder, "Oldnewspapers")
        for image in os.listdir(old_newspapers_dir):
            with open(os.path.join(old_newspapers_dir, image), mode="rb") as img_data:
                self._trainer.create_images_from_data(
                    project.id, img_data.read(), [oldnewspapers_tag.id])

    def train_project(self, project):
        print("Training...")
        try:
            iteration = self._trainer.train_project(project.id)
            while (iteration.status == "Training"):
                iteration = self._trainer.get_iteration(project.id, iteration.id)
                print("Training status: " + iteration.status)
                time.sleep(1)
        except:
            print("No need to retrain. Retrieving default iteration")
            for iteration in trainer.get_iterations(project_id):
                if iteration.is_default:
                    break
        self._trainer.update_iteration(project.id, iteration.id, self._publish_iteration_name, is_default=True)
        print("Done!")
        return project, iteration
    
    def publishIteration(self, project, iteration):
        self._trainer.publish_iteration(project_id=project.id, iteration_id=iteration.id, publish_name=self._publish_iteration_name, prediction_id=self._prediction_resource_id)

    def predict_project(self):
        project = self.find_project()
        with open(os.path.join(self._images_folder, "Test", "test_image-1.jpg"), mode="rb") as test_data:
            results = self._predictor.classify_image(project.id, "Iteration1", test_data.read())

        for prediction in results.predictions:
            print("\t" + prediction.tag_name + ": {0:.2f}%".format(prediction.probability * 100))
    
    def findGeneralCompact(self):
        domain_name = 'General (compact)'
        domain_id = None
        for domain in self._trainer.get_domains():
            if domain.name == domain_name:
                domain_id = domain.id
                print("Found domain: {}  with ID: {}".format(domain_name,domain_id))
                break

        if domain_id == None:
            print("Could not find domain: {}".format(domain_name))
        return domain_id
    
    def changeDomainModel(self, domain_id):
        project_id = None
        project = None
        for prj in self._trainer.get_projects():
            if prj.name == self._sample_project_name:
                project_id = prj.id
                project = prj
                print("Found project: {0}".format(project_id))
                break
                
        if project_id == None:
            print("Could not find your project")

        project.settings.domain_id = domain_id
        project = self._trainer.update_project(project_id, project)
        return project

    def exportIteration(self, project_id, iteration_id):
        print("Requesting export for Iteration ID: {0}".format(iteration_id))
        platform = 'TensorFlow'
        flavor = 'Linux'

        export = self._trainer.export_iteration(project_id, iteration_id, platform)
        while (export.status != 'Done'):
            print("Export status: " + export.status)
            time.sleep(1)
            export = self._trainer.get_exports(project_id, iteration_id)[0]
        print("Export package ready. Download URI: {}", export.download_uri)

        download_filename = 'AIWorkshop.zip'
        print("Downloading from: {0}".format(export.download_uri))
        wget.download(export.download_uri, download_filename)

if __name__ == "__main__":
    cv = CustomVision()
    project = cv.create_project()
    cv.uploadData(project)
    project, iteration = cv.train_project(project)
    # cv.publishIteration(project, iteration)
    # cv.predict_project()
    
    # domain_id = cv.findGeneralCompact()
    # project = cv.changeDomainModel(domain_id)
    # project, iteration = cv.train_project(project)
    # cv.exportIteration(project.id, iteration.id)


