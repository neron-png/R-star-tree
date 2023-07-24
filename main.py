import StorageHandler
import RTree


if __name__ == "__main__":
    StorageHandler.write_blocks_to_datafile()
    StorageHandler.getBlockFromDisk(0)
    RTree.run()

